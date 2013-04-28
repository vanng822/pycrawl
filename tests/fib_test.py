import unittest

import fib

class FibTest(unittest.TestCase):
    
    def test_fib_str(self):
        try:
            fib.fib("10")
            self.fail("Expected un error of TypeError due to requirement of integer in argument")
        except TypeError as e:
            return
        except Exception as e:
            self.fail("Got an unexpected exception %s" % type(e))
            
        self.fail("Shouldn't reach this point. Something is really wrong :-D")
        
    def test_fib(self):
        self.assertEqual(fib.fib(10), 55)