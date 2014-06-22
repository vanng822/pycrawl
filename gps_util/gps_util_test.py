import gps_util
import math
import cProfile

point = {'lat': 59.1929003689438, 'lng': 17.662896132096648}
result = gps_util.get_midpoint([point])
print result
assert result == point

result = gps_util.get_midpoint([point, point])
print result
assert result == point

point1 = {'lat': 59.2, 'lng': 17.2}
point2 = {'lat': 59.4, 'lng': 17.4}

pr = cProfile.Profile()
pr.enable()
for _ in range(100):
    result = gps_util.get_midpoint([point1, point2])
pr.disable()
pr.print_stats()
print result
assert True == (abs(result['lat'] - 59.3) < 0.01)
assert True == (abs(result['lng'] - 17.3) < 0.01)


result = gps_util.get_bounding_box(2.333, 1.000, 20000)
print result

result = gps_util.get_distance(59.19305333867669, 17.661922238767147, 59.192982176318765, 17.662122901529074)
print result
assert result == 13.899604253423052