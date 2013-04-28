import unittest

import fib

class FibTest(unittest.TestCase):
    
    def test_fib(self):
        self.assertEqual(fib.fib(10), 55)