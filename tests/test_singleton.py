from lib import singleton

import unittest

@singleton
class SingletonClass(object):
    def __init__(self):
        self.var1 = 1
        self.var2 = 2


class SingletonTest(unittest.TestCase):
    
    def test_singleton_class(self):
        inst1 = SingletonClass()
        inst2 = SingletonClass()
        inst2.var1 = 10
        inst2.var2 = 20
        
        self.assertEqual(inst1.var1, 10)
        self.assertEqual(inst1.var2, 20)
    