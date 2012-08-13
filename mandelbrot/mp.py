
from multiprocessing import Process

import sys, time
stdout = sys.stdout

BAILOUT = 16
MAX_ITERATIONS = 1000

def iterator(x, y, callback):
    cr = y - 0.5
    ci = x
    zi = 0.0
    zr = 0.0
    i = 0

    while True:
        i += 1
        temp = zr * zi
        zr2 = zr * zr
        zi2 = zi * zi
        zr = zr2 - zi2 + cr
        zi = temp + temp + ci
        
        if zi2 + zr2 > BAILOUT:
            callback(i)
            return
        if i > MAX_ITERATIONS:
            callback(0)
            return


def painting(val):
    if (val == 0):
        stdout.write('*')
    else:
        stdout.write(' ')

class Mandelbrot:
    def __init__(self):
        print 'Rendering...'
        for y in range(-39, 39):
            stdout.write('\n')
            for x in range(-39, 39):
                Process(target=iterator, args=(x / 40.0, y / 40.0, painting, )).start()


t = time.time()
Mandelbrot()
print '\nPython Elapsed %.02f' % (time.time() - t)








