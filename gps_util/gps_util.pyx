
cdef extern from "math.h":
    double asin(double x)
    double sin(double x)
    double cos(double x)
    double sqrt(double x)
    double atan2(double x, double y)
    double fmax(double x, double y)
    double fmin(double x, double y)
    
    const double M_PI
    const double M_PI_2

cdef double EARTH_RADIUS = 6371000
cdef double MIN_LNG = - M_PI
cdef double MAX_LNG = M_PI
cdef double MIN_LAT = - M_PI_2
cdef double MAX_LAT = M_PI_2


cdef double to_rad(double dec_degrees):
    return (dec_degrees * M_PI) / 180

cdef double to_degrees(double radians):
    return (180 * radians) / M_PI

def get_distance(double lat1, double lng1, double lat2, double lng2):
    cdef double delta_lat = to_rad(lat2 - lat1)
    cdef double delta_lng = to_rad(lng2 - lng1)
    cdef double a
    
    a = sin(delta_lat / 2) ** 2 +  cos(to_rad(lat1)) * cos(to_rad(lat2)) * sin(delta_lng / 2) ** 2
    return (2 * atan2(sqrt(a), sqrt(1 - a))) * EARTH_RADIUS

def get_midpoint(list points):
    cdef int plen = len(points)
    
    if plen == 0:
        raise ValueError('Points can not be empty')
    elif plen == 1:
        return points[0]
    
    cdef double x = 0.0, y = 0.0, z = 0.0
    cdef int i
    cdef double lat, lng
    
    for i in range(plen):
        lat = to_rad(points[i]['lat'])
        lng = to_rad(points[i]['lng'])
        x += cos(lat) * cos(lng)
        y += cos(lat) * sin(lng)
        z += sin(lat)
        
    x /= plen
    y /= plen
    z /= plen
    
    return {'lat': to_degrees(atan2(z, sqrt(x * x + y * y))), 'lng': to_degrees(atan2(y, x))}

def get_bounding_box(double lat, double lng, double distance):
    cdef double min_lat, max_lat, min_lng, max_lng
    cdef double delta_lng
    cdef double rad_distance = distance / EARTH_RADIUS
    cdef double rad_lat = to_rad(lat)
    cdef double rad_lng = to_rad(lng)
    
    min_lat = rad_lat - rad_distance
    max_lat = rad_lat + rad_distance
    
    if min_lat > MIN_LAT and max_lat < MAX_LAT:
        delta_lng = asin(sin(rad_distance) / cos(rad_lat))
        min_lng = rad_lng - delta_lng
        if min_lng < MIN_LNG:
            min_lng += 2 * M_PI
        max_lng = rad_lng + delta_lng
        if max_lng > MAX_LNG:
            max_lng -= 2 * M_PI
    else:
        min_lat = fmax(min_lat, MIN_LAT)
        max_lat = fmin(max_lat, MAX_LAT)
        min_lng = MIN_LNG
        max_lng = MAX_LNG
        
    return [
        {'lat': to_degrees(min_lat), 'lng': to_degrees(min_lng)},
        {'lat': to_degrees(max_lat), 'lng': to_degrees(max_lng)}
    ]

