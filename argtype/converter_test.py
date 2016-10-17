from converter import argtype_converter

@argtype_converter(b=bool, s=str)
def testing(b, s):
    print b
    print s


testing(1, 'string')
