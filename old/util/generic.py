import operator as op
import functools as ft

def assure_type(tt, *args, **kwds):
    """Assure that all arguments are of type tt. The variable except can 
    override the default TypeError exception and msg the default message."""
    
    ttst = tt.__name__
    
    # test args
    for i, ar in enumerate(args):
        if not isinstance(ar, tt):
            msg = 'All arguments must be %s, the %sth (%s) is not' % (ttst, i+1, ar)
            raise TypeError(msg)

    for i, (key, ar) in enumerate(kwds.iteritems()):
        if not isinstance(ar, tt):
            msg = 'All arguments must be %s, %s (%s) is not' % (ttst, key, ar)
            raise TypeError(msg)

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
        if not reduce(operator.and_, condition):
            raise exception, msg
    except TypeError:
        # scalar version
        if not condition:
            raise exception, msg
        
def is_var_name(name):
    """Returns True/False if name is a valid python function, variable,
    or attribute name."""
    
    start = name[0] 
    end = name[1:].replace('_', '')
    
    return (start.isalnum() or start == '_') and ( end.isalnum() or len(end) == 0 )

def execute(generator):
    """Consumes the generator.
    
    This function is a sintatic sugar for the common idiom:
        
        execute( x.method() for x in xlist )
    """
    
    tuple(generator)
    
def from_camel_case(st):
    """Translates CamelCase to camel_case"""
    
    ls = list(st)
    for i, c in enumerate(st):
        if c.isupper():
            try:
                if not st[i-1].isupper():
                    ls[i] = '_' + c.lower()
                else:
                    ls[i] = c.lower()
            except:
                pass
    
    res = ''.join(ls)
    return ( res[1:] if res.startswith('_') else res )
