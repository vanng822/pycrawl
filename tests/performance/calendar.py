import cal
import unittest

import cProfile
import camlich

class CalendarTest(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.loop = 1000
    
    def test_amlich(self):
        print 'test_amlich'
        pr = cProfile.Profile()
        pr.enable()
        for i in range(1, self.loop):
            result = cal.amlich.S2L(4, 5, 2013, 7)
            result2 = cal.amlich.L2S(25, 3, 2013, 0, 7)
            
        self.assertEqual(result[0], 25)
        self.assertEqual(result[1], 3)
        self.assertEqual(result2[0], 4)
        self.assertEqual(result2[1], 5)
        pr.disable()
        pr.print_stats()
        
    def test_camlich(self):
        print 'test_camlich'
        pr = cProfile.Profile()
        pr.enable()
        for i in range(1, self.loop):
            result = camlich.solar2lunar(4, 5, 2013, 7)
            result2 = camlich.lunar2solar(25, 3, 2013, 0, 7)
        self.assertEqual(result[0], 25)
        self.assertEqual(result[1], 3)
        self.assertEqual(result2[0], 4)
        self.assertEqual(result2[1], 5)
        pr.disable()
        pr.print_stats()
