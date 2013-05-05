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
            
        self.assertEqual(len(result2), 3)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], 25)
        self.assertEqual(result[1], 3)
        self.assertEqual(result[2], 2013)
        self.assertEqual(result[3], 0)
        self.assertEqual(result2[0], 4)
        self.assertEqual(result2[1], 5)
        self.assertEqual(result2[2], 2013)
        
        pr.disable()
        pr.print_stats()
        
    def test_camlich(self):
        print 'test_camlich'
        pr = cProfile.Profile()
        pr.enable()
        for i in range(1, self.loop):
            result = camlich.solar2lunar(4, 5, 2013, 7)
            result2 = camlich.lunar2solar(25, 3, 2013, 0, 7)
        
        
        self.assertEqual(len(result2), 3)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], 25)
        self.assertEqual(result[1], 3)
        self.assertEqual(result[2], 2013)
        self.assertEqual(result[3], 0)
        self.assertEqual(result2[0], 4)
        self.assertEqual(result2[1], 5)
        self.assertEqual(result2[2], 2013)
        pr.disable()
        pr.print_stats()
        
    def test_cross_check(self):
        dd = 4
        mm = 5
        yy = 2013
        timeZone = 7
        a11 = 24150210
        lunarLeap = 0
        k = 12321434
        dayNumber = 14235435
        jd = 14235435
        self.assertEqual(cal.amlich.jdFromDate(dd, mm, yy), camlich.jd_from_date(dd, mm, yy))
        self.assertEqual(cal.amlich.getLeapMonthOffset(a11, timeZone), camlich.get_leap_month_offset(a11, timeZone))
        self.assertEqual(cal.amlich.getNewMoonDay(k, timeZone), camlich.get_new_moon_day(k, timeZone))
        self.assertEqual(cal.amlich.getSunLongitude(dayNumber, timeZone), camlich.get_sun_longitude(dayNumber, timeZone))
        self.assertEqual(cal.amlich.SunLongitude(jd), camlich.sun_longitude(jd))
        self.assertListEqual(cal.amlich.jdToDate(jd), camlich.jd_to_date(jd))
        self.assertListEqual(cal.amlich.S2L(dd, mm, yy, timeZone), camlich.solar2lunar(dd, mm, yy, timeZone))
        self.assertListEqual(cal.amlich.L2S(dd, mm, yy, lunarLeap, timeZone), camlich.lunar2solar(dd, mm, yy, lunarLeap, timeZone))
        
        
        
        
