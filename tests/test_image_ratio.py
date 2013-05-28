from lib import image_ratio

import unittest

class ImageRatioTest(unittest.TestCase):
    
    def test_image_same_ratio(self):
        r = image_ratio.get_crop_params(1000, 1000, 1)
        self.assertEqual(r.top, 0)
        self.assertEqual(r.left, 0)
        self.assertEqual(r.right, 1000)
        self.assertEqual(r.bottom, 1000)
    
    def test_image_same_ratio_1_2(self):
        r = image_ratio.get_crop_params(1200, 1000, 1.2)
        self.assertEqual(r.top, 0)
        self.assertEqual(r.left, 0)
        self.assertEqual(r.right, 1200)
        self.assertEqual(r.bottom, 1000)
        
    def test_image_larger_ratio(self):
        r = image_ratio.get_crop_params(1000, 600, 1)
        self.assertEqual(r.top, 0)
        self.assertEqual(r.left, 200)
        self.assertEqual(r.right, 800)
        self.assertEqual(r.bottom, 600)
        
    def test_image_smaller_ratio(self):
        r = image_ratio.get_crop_params(600, 1000, 1)
        self.assertEqual(r.top, 200)
        self.assertEqual(r.left, 0)
        self.assertEqual(r.right, 600)
        self.assertEqual(r.bottom, 800)
     
    def test_image_smaller_ratio_1_4(self):
        r = image_ratio.get_crop_params(1000, 1000, 1.4)
        self.assertEqual(r.top, 142)
        self.assertEqual(r.left, 0)
        self.assertEqual(r.right, 1000)
        self.assertEqual(r.bottom, 857)   
    
    def test_image_larger_ratio_1_4(self):
        r = image_ratio.get_crop_params(2000, 1000, 1.4)
        self.assertEqual(r.top, 0)
        self.assertEqual(r.left, 300)
        self.assertEqual(r.right, 1700)
        self.assertEqual(r.bottom, 1000)  