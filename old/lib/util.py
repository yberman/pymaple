from maple import core

def symbol(*args):
    """Creates one or a tuple of symbols from strings on arguments"""
    
    if len(args) > 1:
        return tuple( core.Symbol(x) for x in args )
    else:
        return core.Symbol(args[0])

def srange(*args):
    """Return a tuple of variables name0, name1, name2, etc...
    
    Calling Sequence
    ----------------
    
    srange('x', 3)     =>  (x0, x1, x2)
    srange('x', 1, 4)  =>  (x1, x2, x3)
    srange(3)          =>  (0, 1, 2) # maple integers
    srange(1, 4)       =>  (1, 2, 3) # maple integers
    
    """
    
    if isinstance(args[0], (basestring, core.Symbol)):
        st = str(args[0])
        names = tuple( st + str(i) for i in xrange(*args[1:]) )
        return tuple( symbol(name) for name in names )
    elif isinstance(args[0], (int, core.Rational)):
        N = core.Rational
        return tuple( N(i) for i in xrange(*args[1:]) )
    else:
        msg = 'Invalid types: %s'
        raise TypeError(msg)
 
def div(x, y):
    """Returns the fraction x / y"""
    
    return core.Rational(x, y)

x, y, z = symbol(*'xyz')
I = core.maple('I')
oo = core.maple.infinity
