import unittest
import inspect
import cmandelbrot
from mandelbrot import iterator
import time

import cProfile
 
class MandelbrotTest(unittest.TestCase):
    
    def test_p_c_time(self):
        pr = cProfile.Profile()
        pr.enable()
        t = time.time()
        iterator.Iterator()
        ptotal = time.time() - t
        print '\nMandelbrot Python Elapsed %.06f' % ptotal
        pr.disable()
        pr.print_stats()
        
        pr = cProfile.Profile()
        pr.enable()
        t = time.time()
        cmandelbrot.mandelbrot()
        ctotal = time.time() - t
        
        print '\nC Mandelbrot Python Elapsed %.06f' % ctotal
        
        pr.disable()
        pr.print_stats()
        
        print '\n %f times slower' % (ptotal / ctotal)
        
        self.assertTrue(ctotal < ptotal)
        
    def test_c_p_time(self):
        pr = cProfile.Profile()
        pr.enable()
        t = time.time()
        cmandelbrot.mandelbrot()
        ctotal = time.time() - t
        print '\nC Mandelbrot Python Elapsed %.06f' % ctotal
        pr.disable()
        pr.print_stats()
        
        
        pr = cProfile.Profile()
        pr.enable()
        t = time.time()
        iterator.Iterator()
        ptotal = time.time() - t
        print '\nMandelbrot Python Elapsed %.06f' % ptotal
        pr.disable()
        pr.print_stats()
        print '\n %f times slower' % (ptotal / ctotal)
        
        self.assertTrue(ctotal < ptotal)
