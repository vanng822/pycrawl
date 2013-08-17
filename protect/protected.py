

import inspect


class Protected(object):
    
    _do_not_touch = None
    
    @property
    def do_not_touch(self):
        return self._do_not_touch
    
    @do_not_touch.setter
    def do_not_touch(self, value):
        
        currentframe = inspect.currentframe()
        calframe = inspect.getouterframes(currentframe, 2)
        
        caller_name = calframe[1][3]
        
        if caller_name != 'logic_set_do_not_touch':
            raise Exception('Not allow to set value outside logic_set_do_not_touch')
        
        self._do_not_touch = value