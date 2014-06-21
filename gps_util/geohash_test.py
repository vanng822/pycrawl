import geohash
import cProfile

pr = cProfile.Profile()
pr.enable()
for _ in range(10000):
    result = geohash.encode(57.64911, 10.40744, 11)
pr.disable()
pr.print_stats()

print result

assert result == 'u4pruydqqvj'


result = geohash.decode('u4pruydqqvj')
print result
