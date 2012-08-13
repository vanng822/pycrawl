
from threading import Thread

import sys, time
stdout = sys.stdout

BAILOUT = 16
MAX_ITERATIONS = 1000

def iternator(x, y, callback):
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
            callback(i, x, y)
            return
        if i > MAX_ITERATIONS:
            callback(0, x, y)
            return

def painting(val, x, y):
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
                #stdout.write('%d, %d' % (x, y))
                Thread(target=iternator, args=(x / 40.0, y / 40.0, painting, )).start()
                #print x
                
t = time.time()
Mandelbrot()

print '\nPython Elapsed %.02f' % (time.time() - t)
