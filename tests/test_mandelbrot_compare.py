import unittest
import inspect
import cmandelbrot
from mandelbrot import iterator
import time
 
class MandelbrotTest(unittest.TestCase):
    
    def test_p_c_time(self):
        t = time.time()
        iterator.Iterator()
        ptotal =  time.time() - t
        print '\nMandelbrot Python Elapsed %.06f' % ptotal
        
        t = time.time()
        cmandelbrot.mandelbrot()
        ctotal = time.time() - t
        
        print '\nC Mandelbrot Python Elapsed %.06f' % ctotal
        print '\n %f times slower' % (ptotal/ctotal)
        
        self.assertTrue(ctotal < ptotal)
        
    def test_c_p_time(self):
        
        t = time.time()
        cmandelbrot.mandelbrot()
        ctotal = time.time() - t
        print '\nC Mandelbrot Python Elapsed %.06f' % ctotal
        
        t = time.time()
        iterator.Iterator()
        ptotal =  time.time() - t
        print '\nMandelbrot Python Elapsed %.06f' % ptotal
        
        print '\n %f times slower' % (ptotal/ctotal)
        
        self.assertTrue(ctotal < ptotal)