import kernel
from kernel import MaplePtr

# ---------------------------------------------------------------------------- #
# Base Maple object
# ---------------------------------------------------------------------------- #

class Maple(object):
    _PY_CLASSES = { 
       kernel.EXPSEQ: tuple,
       kernel.LIST: list,
       kernel.SET: set,
       kernel.STRING: str,
       #kernel.MODULE: 'module', #TODO
       #kerne0l.RTABLE: 'rtable', 
       }
    
    def __new__(cls, cmd='', _ptr=None, _klass=None, *args, **kwds):
        '''Return object resulting from Maple command 'cmd'. Notice that it is 
        not necessary that the constructor return an instance of Maple. 
        Automatic conversion to python objects is in place, e.g., Maple('"foo"')
        will return a regular python string.'''
        
        # inititialization of maple object
        if isinstance(_ptr, MaplePtr):
            # binds to MaplePtr
            ptr = _ptr
        else:
            # initializes from ptr or command
            ptr = MaplePtr(cmd=cmd, ptr=_ptr)
            
        # query the object type
        if _klass:
            cls = _klass
        else:
            idx = ptr.type()
            cls = Maple._PY_CLASSES.get(idx, Maple)
        
        # initializes object
        if Maple in cls.__bases__ or cls is Maple:
            obj = object.__new__(cls)
            obj._maple_ptr = ptr
            return obj
        else:    
            # convert to python objects
            if idx == kernel.EXPSEQ:
                return tuple( Maple(_ptr=x) for x in  ptr.data() )
            
            elif idx == kernel.LIST:
                data = MaplePtr(ptr=ptr.data()[0]).data()
                return [ Maple(_ptr=x) for x in data ]
            
            elif idx == kernel.SET:
                data = MaplePtr(ptr=ptr.data()[0]).data()
                return set( Maple(_ptr=x) for x in data )
                
            elif idx == kernel.STRING:
                return str(ptr)
            
            elif idx == kernel.MODULE:
                raise NotImplementedError
            
            elif idx == kernel.RTABLE:
                raise NotImplementedError
            
            else:
                raise RuntimeError('Unknown maple object of type "%s"' % MaplePtr('whattype')(ptr))
        
    def __repr__(self): return repr(self._maple_ptr)
    def __str__(self): return str(self._maple_ptr)
    def __hash__(self): return hash(str(self))
        
    def __pow__(self, other, mod=None): 
        if mod is None:
            return self.__pow_simple__(other)
        else:
            return self.__pow_simple__(other) % mod

    def __call__(self, *args, **kwds):
        if kwds:
            args = list(args)
            for k,v in kwds.items():
                if isinstance(v, basestring):
                    v = Maple(v)
                args.append(Maple(k)==v)
        ptr = self._maple_ptr(*args)
        if ptr is not None:
            return Maple(_ptr=ptr)
                
    def __nonzero__(self):
        """x.__nonzero__() <==> bool(x)"""
        #TODO: define nonzero
        if str(Maple('is')(self)) == 'true':
            return True
        else:
            return False
            
    def __eq__(self, other):
        #TODO: define nonzero
        if isinstance(other, bool):
            return self.__nonzero__() == other
        else:
            return self.__eq_simple__(other)

    def __getstate__(self):
        return str(self)
    
    def __setstate__(self, cmd):
        obj = Maple(cmd=cmd)
        self.__dict__.update(obj.__dict__)

    #--- type conversion ------------------------------------------------------#
    #TODO:FIXME: hackish, ugly... 
    def __int__(self):
        try:
            return int(float(self))
        except TypeError, e:
            raise e("Maple object '%s' cannot be converted to int" % self)

    def __float__(self):
        try:
            return float(str(self.evalf()))
        except TypeError, e:
            raise e("Maple object '%s' cannot be converted to int" % self)

    #--- documentation --------------------------------------------------------#
    #TODO: it is not working! why?
                    
    #--- API ------------------------------------------------------------------#
    def eval(self, *args, **kwds):
        """Evaluates expression with substitutions
        
        The eval method is used to evaluate an expression at a given point 
        and to finish incomplete evaluations. We show some examples of both
        uses:
        
        Substitutions
        -------------
        
        >>> expr = x*y
        >>> expr.eval(x==z, y==Pi)
        z * Pi
        
        Finish an incomplete evaluation
        -------------------------------
        
        >>> expr = maple("'exp(0)'")
        >>> print expr, expr.eval()
        exp(0) 1
                
        Arguments
        ---------
        
        A list of relations of the type a==b, in which values of a are 
        substituted in expression to b. An optional call is used to perform
        multiple incomplete evaluations is done by setting the keyword
        levels equal to the number of multiple evaluations."""
        
        #args = pyargs_to_cargs(args, kwds)
        
        #if not args:
        #    return algeb(M.MapleEval(KV, self._obj))
        #elif len(args) == 1:
        #    return __eval__(self, args[0])
        #else:
        #    return __eval__(self, list(args))
        pass

    def evalf(self, *args, **kwds):
        """Evaluates expression using floating-point arithmetics.
        
        Similar to the eval method, it accepts the same arguments. 
        The answer is evaluated to a python float else it raises a TypeError exception."""
        #FIXME: trap errors in libmaplec.evalhf
        #make substituitions
        
        if args or kwds:
            return self.eval(*args, **kwds).evalhf()
        else:
            return Maple('evalf')(self)
        
    def evalhf(self, *args, **kwds):
        """Evaluates expression using hardware floats.
        
        Similar to the eval method, it accepts the same arguments. 
        The answer is evaluated to a python float else it raises a TypeError exception."""
        #FIXME: trap errors in libmaplec.evalhf
        #make substituitions
        
        if args or kwds:
            return self.eval(*args, **kwds).evalhf()
        else:
            return Maple('evalhf')(self)
    
# ---------------------------------------------------------------------------- #
# Proxy object
# ---------------------------------------------------------------------------- #

class Proxy(object):
    def __init__(self, *args, **kwds):
        self._args = args
        self._kwds = kwds
    
    def initialize(self):
        obj = Maple(*self._args, **self._kwds)
        del self._args
        del self._kwds
        self.__class__ = obj.__class__
        self.__dict__.update(obj.__dict__)
        
    def __getattr__(self, attr):
        self.initialize()
        return getattr(self, attr)
    
    def __call__(self, *args, **kwds):
        self.initialize()
        return self(*args, **kwds)
    
    def __repr__(self):
        self.initialize()
        return repr(self)
    
    def __str__(self):
        self.initialize()
        return str(self)
    
# ---------------------------------------------------------------------------- #
# Define extra methods to be used by Maple() that depends on basic Maple() 
# functionality

def maplef(cmd):
    obj = Proxy(cmd)
    def method(*args, **kwds):
        return obj(*args, **kwds)
    return method
    
# mathematical operations -----------------------------------------------------#
Maple.__add__ = Maple.__radd__ = maplef('`+`')
Maple.__mul__ = Maple.__rmul__ = maplef('`*`')
Maple.__sub__ = maplef('(x, y) -> x - y')
Maple.__rsub__ = maplef('(x, y) -> y - x')
Maple.__div__ = maplef('(x, y) -> x / y')
Maple.__rdiv__ = maplef('(x, y) -> y / x')
Maple.__pow_simple__ = maplef('`^`') # fix this!
Maple.__mod__ = Maple.__rmod__ = maplef('(x, y) -> x mod y')
Maple.__pos__ = maplef('x -> + x')
Maple.__neg__ = maplef('x -> - x')
Maple.__fat__ = maplef('x -> x!')
Maple.__dot__ = Maple.__rdot__ = maplef('(x, y) -> x.y')
    
#--- logical operations -------------------------------------------------------#
Maple.__not__ = maplef('x -> not x')
Maple.__and__ = maplef('(x, y) -> x and y')
Maple.__or__ = maplef('(x, y) -> x or y')
Maple.__xor__ = maplef('(x, y) -> x xor y')
Maple.__implies__ = maplef('(x, y) -> x implies y')

#--- comparison operators -----------------------------------------------------#
Maple.__lt__ = maplef('(x, y) -> x < y')
Maple.__le__ = maplef('(x, y) -> x <= y')
Maple.__gt__ = maplef('(x, y) -> x > y')
Maple.__ge__ = maplef('(x, y) -> x >= y')
Maple.__eq_simple__ = maplef('(x, y) -> x = y')
Maple.__ne__ = maplef('(x, y) -> x <> y')
Maple.__is__ = maplef('is')

#--- evaluation functions -----------------------------------------------------#
Maple.__eval__ = maplef('eval')
Maple.__evalhf__ = maplef('evalhf')

#--- list interface -----------------------------------------------------------#
Maple.__getitem__ = maplef('(x, i) -> x[i]')
Maple.__contains__ = maplef('(l, x) -> x in l')

"""    
# set operators -----------------------------------------------------------#
__union__ = maplef('(x, y) -> x union y')
__subset__ = maplef('(x, y) -> x subset y')
__intersect__ = maplef('(x, y) -> x intersect y')
__minus__ = maplef('(x, y) -> x minus y')
__in__ = maplef('(x, y) -> x in y')

# misc operators ----------------------------------------------------------#
__seq__ = maplef('`$`')
__arrow__ = maplef('(x, y) -> (x -> y)')
__compose__ = maplef('`@`')
__rcompose__ = maplef('`@@`')
__concat__ = maplef('`||`')
__range__ = maplef('`..`')
__type__ = maplef('`::`')
__mod_member__ = maplef('`:-`')

#__assuming__ 
# __index__, __truediv__, __abs__, __floordiv__, __invert__(~x),
# __contains__, __iadd__, __isub__, 
# bitwise ops: a&b, a^b, a|b, and ~a, a>>b, a<<b 
"""

def register(cmd, cls):
    """Register the type of object resulting from cmd to the Python class 
    cls."""
    
    idx = kernel.ctype(cmd)
    Maple._PY_CLASSES[idx] = cls
    
# ---------------------------------------------------------------------------- #
# Default Maple interpreter

class Interpreter(object):
    def __call__(self, cmd):
        return Maple(cmd=str(cmd))

    def __getattr__(self, attr):
        if not attr.startswith('_'):
            return Maple(cmd=attr)
        else:
            raise AttributeError

maple = Interpreter()
