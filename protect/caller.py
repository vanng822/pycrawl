import logic

def set_outside_logic(protected):
    protected.do_not_touch = 'OUTSIDE'

def set_from_logic(protected):
    logic.logic_set_do_not_touch(protected, 'CALLER VIA LOGIC')