"""Small functions that do simple and useful things."""
import operator as _op

def assure(condition, exception=AssertionError, msg=''):
    """Assure condition (or list of conditions) holds, otherwise
    raise exception.
    
    Inputs:
    
    @param condition: condition or iterable list of conditions  
    @param exception: exception that shall be raised case conditions fail
    @param msg: message raised with exception
    """
    
    try:
        # iterator version of the function
        if not reduce(_op.and_, condition):
            raise exception, msg
    except TypeError:
        # scalar version
        if not condition:
            raise exception, msg
        
def is_var_name(name):
    """Returns True/False if name is a valid python function, variable,
    or attribute name."""
    
    # define the valid characters
    valid_chars = 'abcdefghijklmnopqrstuvwxyz'
    valid_chars += valid_chars.upper() + '_'
    
    # test it!
    try:
        assure(( x in valid_chars for x in name ), ValueError)
        return True
    except ValueError:
        return False

def execute(generator):
    """Consumes the generator.
    
    This function is a sintatic sugar for the common idiom:
        
        execute( x.method() for x in xlist )
    """
    for x in generator:
        pass

##############################################################################
#
#        COMPARISON OR NONE FUNCTIONS
#
##############################################################################
def _factory(cmp_f):
    # comparison factory
    def func(value, number):
        try:
            value = ( x for x in value if not x is None )
            return reduce(_op.and_, ( cmp_f(x, number) for x in value ))
        except TypeError:
            return value > number
    
    return func
    
ge_or_none = _factory(lambda x, y: x >= y)
"""True if all values are greater or equal than number or equal to None"""

gt_or_none = _factory(lambda x, y: x > y)
"""True if all values are greater than number or equal to None"""

le_or_none = _factory(lambda x, y: x <= y)
"""True if all values are lesser or equal than number or equal to None"""

lt_or_none = _factory(lambda x, y: x < y)
"""True if all values are lesser than number or equal to None"""

