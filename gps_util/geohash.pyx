

base32_string = '0123456789bcdefghjkmnpqrstuvwxyz'

def encode(double lat, double lng, int precision = 12):
	cdef list geohash = []
	cdef list bits = [16, 8, 4, 2, 1]
	
	cdef double max_lat = 90, min_lat = -90
	cdef double max_lng = 180, min_lng = -180
	cdef int even = 1
	cdef int bit, hash_pos, len_counter = 0
	cdef double mid
	
	while len_counter < precision:
		hash_pos = 0
		for bit in range(5):
			if even:
				mid = (max_lng + min_lng) / 2
				if lng > mid:
					hash_pos |= bits[bit]
					min_lng = mid
				else:
					max_lng = mid
			else:
				mid = (max_lat + min_lat) / 2
				if lat > mid:
					hash_pos |= bits[bit]
					min_lat = mid
				else:
					max_lat = mid
			even = 0 if even == 1 else 1
			
		geohash.append(base32_string[hash_pos])
		len_counter += 1
	
	return ''.join(geohash)

def decode(hash):
	cdef double max_lat = 90, min_lat = -90
	cdef double max_lng = 180, min_lng = -180
	cdef int i, even = 1, hash_pos, bit
	cdef double mid, lat, lng
	
	for i in range(len(hash)):
		hash_pos = base32_string.index(hash[i])
		for bit in range(4, -1, -1):
			if even == 1:
				mid = (max_lng + min_lng) / 2
				if ((hash_pos >> bit) & 1) == 1:
					min_lng = mid
				else:
					max_lng = mid
			else:
				mid = (max_lat + min_lat) / 2
				if ((hash_pos >> bit) & 1) == 1:
					min_lat = mid
				else:
					max_lat = mid
			even = 0 if even == 1 else 1
	
	lat = (min_lat + max_lat) / 2
	lng = (min_lng + max_lng) / 2
	
	return {
		'lat': lat,
		'lng': lng,
		'error': {
			'lat': max_lat - lat,
			'lng': max_lng - lng
		}
	}
	