import unittest

import fib

class FibTest(unittest.TestCase):
    
    def test_fib_str(self):
        try:
            fib.fib("10")
            self.fail("Expected un error of TypeError due to requirement of integer in argument")
        except TypeError as e:
            pass
        
    def test_fib(self):
        self.assertEqual(fib.fib(10), 55)