


import protected
import logic
import caller

t = protected.Protected()
try:
    t.do_not_touch = 'DSDFD'
except Exception, e:
    print e.message

assert t.do_not_touch == None

logic.logic_set_do_not_touch(t, 'SET BY LOGIC')

assert t.do_not_touch == 'SET BY LOGIC'

try:
    caller.set_outside_logic(t)
    
except Exception, e:
    print e.message

assert t.do_not_touch == 'SET BY LOGIC'

caller.set_from_logic(t)

assert t.do_not_touch == 'CALLER VIA LOGIC'