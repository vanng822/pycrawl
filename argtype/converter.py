import functools
import inspect

def argtype_converter(**vartypes):
    """ vartypes: key value where key is argument name and value is type of it
        for example @argtype_converter(silent=bool, server=string)
    """
    def inner_argtype_converter(func):

        """ Checking if all varnames are valid
        """
        for varname in vartypes:
            if varname not in func.func_code.co_varnames:
                raise KeyError('variable name: {varname} does not exist'.format(varname=varname))

        def bool_converter(value):
            """ Special boolean handling for our case
            """
            if value in (False, 'False', 'false', 0, '0'):
                return False
            elif value in (True, 'True', 'true', 1, '1'):
                return True
            return value

        def convert(value, vartype):
            if vartype is bool:
                return bool_converter(value)
            else:
                return vartype(value)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            (func_args, _, _, func_defaults) = inspect.getargspec(func)
            if func_defaults:
                arg_length = len(func_args) - len(func_defaults)
            else:
                arg_length = len(func_args)

            arg_names = func_args[:arg_length]
            # need new args since it is inmutable
            new_args = ()
            for i, arg_name in enumerate(arg_names):
                value = args[i]
                if arg_name in vartypes:
                    value = convert(value, vartypes[arg_name])
                new_args += (value,)

            # just modified same kwargs
            for arg_name in kwargs:
                if arg_name in vartypes:
                    kwargs[arg_name] = convert(kwargs[arg_name], vartypes[arg_name])

            return func(*new_args, **kwargs)

        return wrapper

    return inner_argtype_converter
