import unittest

import cProfile
import re
import string

class ReplaceTest(unittest.TestCase):
    
    def setUp(self):
        self.test_str = 'test and testing for the performance test'
        self.test_replaces = 'test for performance'.split(' ')
        self.run_times = 2000
        self.multi = 100
    
    def multi_str(self):
        test_str = ''
        for i in range(1, self.multi):
            test_str += ' ' + self.test_str
        
        return ' ' + test_str + ' '
    
    def test_string_replace(self):
        print 'test_string_replace'
        pr = cProfile.Profile()
        pr.enable()
        
        for i in range(1, self.run_times):
            str = self.multi_str()
            for t in self.test_replaces:
                str = string.replace(str, ' ' + t + ' ', ' {' + t + '} ')
                #print str
                
        pr.disable()
        pr.print_stats()
        
    def test_re_replace(self):
        print 'test_re_replace'
        
        pr = cProfile.Profile()
        pr.enable()
        for i in range(1, self.run_times):
            str = self.multi_str()
            for t in self.test_replaces:
                str = re.sub(' (' + t + ') ', r' {\1} ', str)
                #print str
        pr.disable()
        pr.print_stats()
        
        
        