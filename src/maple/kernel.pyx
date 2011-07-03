cimport openmaple as M
from openmaple cimport ALGEB
import os
import config

#------------------------------------------------------------------------------#
# Kernel callbacks
#------------------------------------------------------------------------------#
MAPLE_TEXT_CALLBACK_TAGS = {
    3: 'OUTPUT',  # A line-printed (1-D) Maple expression or statement.       
                                                                            
    1: 'DIAG',    # Diagnostic output (high printlevel or trace output). 
    
    2: 'MISC',    # Miscellaneous output, for example, from the Maple     
                  # printf function.                                      
                    
    9: 'HELP',    # Text help output. This is generated in response to a  
                  # help request.  For a more comprehensive help          
                  # facility, see MapleHelp.                              
                    
    4: 'QUIT',    # Response to a Maple quit, done, or stop command.      
    
    5: 'WARNING', # A warning message generated during a computation.     
    
    6: 'ERROR',   # An error message generated during parsing or          
                  # processing. This is generated only if you             
                  # do not specify an errorCallBack function.             
                    
    7: 'STATUS',  # Kernel resource usage status (a "bytes used"          
                  # message). This is generated only if you               
                  # do not specify a statusCallBack function.
                    
    10: 'DEBUG'   # Output from the Maple debugger.   
}

HELP = []
MISC = []
STATUS = []
cdef int WORDSIZE = int(os.environ.get('WORDSIZE', 32))

#------------------------------------------------------------------------------#
# Error Handling
#------------------------------------------------------------------------------#

class MapleError(Exception): 
    pass
    
class UnknownMapleError(MapleError): 
    pass    

cdef void textCallBack(void* data, int tag, char* output):
    """Callback used for directing result output"""

    if MAPLE_TEXT_CALLBACK_TAGS[tag] == 'OUTPUT' or MAPLE_TEXT_CALLBACK_TAGS[tag] == 'MISC':
        print output
    elif MAPLE_TEXT_CALLBACK_TAGS[tag] == 'HELP':    
        HELP.append(output)
    elif MAPLE_TEXT_CALLBACK_TAGS[tag] == 'STATUS':
        STATUS.append(output)
    else:
        print '%s: %s' % (MAPLE_TEXT_CALLBACK_TAGS[tag], output)

cdef void errorCallBack(void *data, M.M_INT offset, char *cmsg):
    """C-code cannot raise Python exceptions. This callback store the last 
    Maple exception to be re-raised in Python code when we check for its 
    existence."""
    
    # KV_EXCEPTION must be empty. 
    # Not being so indicates an unhandled exception, which is a bug, 
    # so we must warn the user.
    global KV_EXCEPTION
    if KV_EXCEPTION:
        print 'Warning: Unhandled exception "%s"' % KV_EXCEPTION	
    
    msg = cmsg
    msg = msg.strip('Error, ')
    if offset < 0:
        # Maple exceptions are strings. We must try to infer the error from 
        # the error message
        KV_EXCEPTION = MapleError(msg)
    else:
        # this is a syntax error
        # put ^^^ under the original input to indicate where 
        # the syntax error probably was
        msg = "Syntax Error, %s" % msg
        msg += '\n' + ' ' * offset + '^^^'
        KV_EXCEPTION = SyntaxError(msg)
    
# statusCallBack not used
# readLineCallBack not used
# redirectCallBack not used
# streamCallBack not used
# queryInterrupt not used
# callBackCallBack not used

#------------------------------------------------------------------------------#
# KernelVector initializer
#------------------------------------------------------------------------------#
cdef char KV_err[2048] # error buffer
KV_EXCEPTION = None

# Kernel starter
cdef M.MKernelVector kernel_init():
    """Starts Maple Kernel and returns the pointer to MKernelVector
    """
    
    #os.environ['MAPLE'] = config.MAPLE_PATH
    cdef M.MKernelVector kv
    cdef M.MCallBackVectorDesc cbv
    cbv.textCallBack = textCallBack
    cbv.errorCallBack = errorCallBack
    cbv.statusCallBack = NULL
    cbv.readLineCallBack = NULL
    cbv.redirectCallBack = NULL
    cbv.streamCallBack = NULL
    cbv.queryInterrupt = NULL
    cbv.callBackCallBack = NULL
    kv = M.StartMaple(0, NULL, &cbv, NULL, NULL, KV_err)
    if <void *> kv == NULL:
        raise RuntimeError('Fatal error, %s' % KV_err)
    
    return kv

cdef M.MKernelVector KV = kernel_init()

#------------------------------------------------------------------------------#
# Utility functions
#------------------------------------------------------------------------------#
def maple_help(obj):
    """Return the help output for Maple object or command"""
    
    global HELP
    HELP[:] = []
    if isinstance(obj, basestring):
        obj = MaplePtr(cmd=obj)
    
    MaplePtr(cmd='help')(obj)
    ret = '\n'.join(HELP)
    HELP[:] = []
    return ret

def maple_misc():
    """empty and return the maple misc output"""
    
    global MISC
    ret = '\n'.join(MISC)
    MISC[:] = []
    return ret

def pop_error():
    """return last error and clean KV_EXCEPTION"""

    global KV_EXCEPTION
    if KV_EXCEPTION:
        ex = KV_EXCEPTION
        KV_EXCEPTION = None
        return ex
    else:
        raise RuntimeError('Trying to raise empty Maple error.')

#------------------------------------------------------------------------------#
# Base Maple type
#------------------------------------------------------------------------------#

# python object type
cdef int PYOBJTYPE
PYOBJTYPE = <int> kernel_init # unique integer identifier (can be any arbitrary c-function)

# MaplePointer mark/dispose/print functions
cdef void _dispose_function(ALGEB mptr) nogil:
    #M.MapleGcAllow(KV, <ALGEB> M.MapleToPointer(KV, mptr))
    pass

cdef void _mark_function(ALGEB mptr) nogil:
    M.MapleGcMark(KV, <ALGEB> M.MapleToPointer(KV, mptr))

cdef ALGEB _print_function(ALGEB mptr) nogil:
    return <ALGEB> M.MapleToPointer(KV, mptr)
    
cdef class MaplePtr:
    cdef ALGEB _obj
    cdef ALGEB _mptr
    OBJECTS = {}
    
    def __cinit__(self, cmd='', ptr=None):
        """This is the parent class of all Maple objects. Its ensures that 
        Maple ALGEB objects are not garbage collected when referenced by 
        a Python object. Hence all Python references to Maple objects must
        use MaplePtr objects.
        
        The constructor also binds the python instance to an ALGEB object 
        defined in C. This method is safe since it prevents Maple's own GC from
        trashing the reference to a living Python wrapper and also prevents 
        intialization from a NULL pointer.
        
        If cmd is given, it evaluates Maple command and returns the output. If
        ptr is given, it creates a Python wrapper to Maple's object ptr. If 
        both parameters are defined, the contructor raises a ValueError. 
        """
        aux = ( ptr if ptr is not None else <int> NULL ) 
        self._obj = <ALGEB><int> aux
        self._mptr = NULL
        
        if cmd and (ptr is not None):
            raise TypeError('The "ptr" and "cmd" arguments cannot be defined simultaneously') 
        elif cmd:
            cmd = ( cmd if cmd[-1] in [ ':', ';'] else cmd + ':' )
            self._obj = M.EvalMapleStatement(KV, cmd)
        elif ptr is None:
            raise TypeError('Either "ptr" or "cmd" must be given to initialize MaplePtr object')
        elif ptr:
            self._obj = <ALGEB><int>ptr
        elif ptr == 0:
            raise ValueError('Trying to initialize MaplePtr from null pointer')
        else:
            raise RuntimeError
            
        #print 'starting from pointer'
        if self._obj == NULL:
            ex = pop_error()
            if cmd:
                msg = str(ex)
                msg += '\n (Error found evaluating command "%s")' % cmd
                if len(ex.args) > 1:
                    ex = type(ex)(msg, *ex.args[1:])
                else:
                    ex = type(ex)(msg)
            raise ex
                   
        # creates a maple pointer that holds an address to obj
        self._mptr = M.ToMaplePointer(KV, <void*> self._obj, PYOBJTYPE)
        M.MaplePointerSetMarkFunction(KV, self._mptr, _mark_function)
        M.MaplePointerSetPrintFunction(KV, self._mptr, _print_function)
        M.MaplePointerSetDisposeFunction(KV, self._mptr, _dispose_function)
        M.MapleGcProtect(KV, self._mptr)
            
    def __dealloc__(MaplePtr self):
        # free memory of correctly initialized objects
        if self._mptr != NULL:
            M.MapleGcAllow(KV, self._mptr)
    
    def __repr__(MaplePtr self):
        cdef MaplePtr aux
        
        # special case exprseq's 
        if M.IsMapleExpressionSequence(KV, self._obj):
            return repr(MaplePtr(cmd='`[]`')(self))[1:-1]
        else:
            aux = self.OBJECTS['convert_str'](self)
            return M.MapleToString(KV, aux._obj)
            
    def __str__(self):
        return repr(self)
        
    def __call__(self, *args):
        """The call method first convert all python object to appropriate 
        ALGEB's, evaluate the expression using EvalMapleProc, and then 
        convert the output to an appropriate Python oprint '%s: %s' % (MAPLE_TEXT_CALLBACK_TAGS[tag], output)bject."""
        
        cdef MaplePtr seq = MaplePtr(ptr=<int>M.NewMapleExpressionSequence(KV, len(args)))
        cdef MaplePtr aux
        cdef int res_ptr
        
        for i, arg in enumerate(args):
            aux = self.py_to_c(arg)
            M.MapleExpseqAssign(KV, seq._obj, i + 1, aux._obj)
        
        res_ptr = <int> M.EvalMapleProcedure(KV, self._obj, seq._obj)

        if <int> M.IsMapleNULL(KV, <ALGEB> res_ptr):
            return None
        elif res_ptr != 0:
            return MaplePtr(ptr=res_ptr)
        else:
            ex =  pop_error()
            msg = 'Error calling %s(%s):\n    %s' % (self, str(args)[1:-1], ex)
            raise MapleError(msg)
    
    cpdef address(self): return <int> self._obj

    def ast(MaplePtr self):
        pass
        
    def ast_iter(MaplePtr self):
        pass
    
    #def __iter__(MaplePtr self):
    #    cdef MaplePtr aux
    #    type_no = int(str(self.OBJECTS['get_type'](self)))
    #    
    #    if type_no == EXPSEQ:
    #        print 'expseq', self
    #        raise Exception
    #    elif type_no == LIST:
    #        print 'list', self
    #        raise Exception
    #    else:
    #        raise TypeError('Object of type %s is not iterable' % self.OBJECTS['whattype'](self))
    
    def internal_repr(MaplePtr self):
        '''Prints information about the internal representation of object'''
        cdef int aux 
        print '\nobject:', self
        aux = <int> self._obj
        print 'address:\t%s\t(%s)' % (aux, bitrepr(aux, 32))
        print 'header:\t\t%s\t(%s)' % (self.header(), bitrepr(self.header(), 32))
        print 'mtype:\t\t', self.type()
        print 'word size:\t', self.size()
    
    def header(MaplePtr self):
        '''Maple uses the first 6 bits from the header to store type 
        information. If the addres is odd, it represents an integer.'''
        
        # odd pointers represent integers
        if <int> self._obj % 2 == 1 or <int> self._obj < 0:
            return None
        elif self._obj == NULL:
            raise ValueError('Invalid object at %s' % <int> self._obj)
        else:
            return <int> self._obj[0]
    
    def type(MaplePtr self):
        '''Maple uses the first 6 bits from the header to store type 
        information. If the addres is odd, it represents an integer.'''
        
        cdef int aux
        
        try:
            aux = <int> self.header()
            if aux > 0:
                return aux >> (WORDSIZE - 6)
            else:
                return 63 - ((-aux) >> (WORDSIZE - 6))
        except TypeError:
            aux = <int> self._obj
            if aux > 0:
                return 2 # INTPOS
            else:
                return 1 # INTNEG
    
    def size(MaplePtr self):
        '''Maple uses the last 6 bits from the header to store lenght 
        information'''
        
        cdef int aux
        
        try:
            aux = <int> self.header()
            if aux > 0:
                return aux % (2**(WORDSIZE - 6))
            else:
                return 2**(WORDSIZE - 6) - (-aux) % (2**(WORDSIZE - 6))
        except TypeError:
            return None
            
    def data(MaplePtr self):
        '''Return a list of integers representing the words in object's data 
        structure'''
        
        try:
            return tuple([ <int> self._obj[i] for i in xrange(1, self.size()) ])
        except:
            return None
    
    cpdef MaplePtr py_to_c(self, py):
        """Convert python objects to the corresponding Maple ones."""
        
        cdef MaplePtr ret
        cdef MaplePtr aux
        try:
            ret = py._maple_ptr
            return ret
        except AttributeError:
            try:
                ret = py
                return ret
            except:
                pass
                
            if isinstance(py, int):
                ret = MaplePtr(ptr=<int>M.ToMapleInteger(KV, py))
                
            elif isinstance(py, long):
                ret = MaplePtr(cmd=str(py).rstrip('L'))  
                
            elif isinstance(py, float):
                return MaplePtr(ptr=<int>M.ToMapleFloat(KV, py))
                
            elif isinstance(py, complex):
                f = MaplePtr('(x,y) -> x + I*y')
                return f(py.real, py.imag)
                
            elif isinstance(py, basestring):
                ret = MaplePtr(ptr=<int>M.ToMapleString(KV, py))
                
            elif isinstance(py, bool):
                if py:
                    ret = MaplePtr(ptr=<int>M.ToMapleBoolean(KV, 1))
                else:
                    ret = MaplePtr(ptr=<int>M.ToMapleBoolean(KV, 0))
                    
            elif py is None:
                ret = MaplePtr(ptr=<int>M.ToMapleNULL(KV))
                
            elif isinstance(py, tuple):
                objs = iter(py)
                ret = MaplePtr(ptr=<int>M.NewMapleExpressionSequence(KV, len(py)))
                for 1 <= i <= len(py):
                    aux = self.py_to_c(objs.next())
                    M.MapleExpseqAssign(KV, ret._obj, i, aux._obj)

            elif isinstance(py, list):
                ret = self.py_to_c(tuple(py))
                aux = MaplePtr('`[]`')
                ret = MaplePtr(ptr=<int>M.EvalMapleProcedure(KV, aux._obj, ret._obj))

            elif isinstance(py, set):
                ret = self.py_to_c(tuple(py))
                aux = MaplePtr('`{}`')
                ret = MaplePtr(ptr=<int>M.EvalMapleProcedure(KV, aux._obj, ret._obj))
                
            else:
                raise TypeError('Object type <%s> does not exist in Maple' % type(py))

        return ret


# Fill MaplePtr.OBJECTS dictionary
MaplePtr.OBJECTS['convert_str'] = MaplePtr(cmd='x -> convert(x, string)')
MaplePtr.OBJECTS['nops'] = MaplePtr(cmd='nops')
MaplePtr.OBJECTS['op'] = MaplePtr(cmd='op')
MaplePtr.OBJECTS['to_list'] = MaplePtr(cmd='`[]`')
MaplePtr.OBJECTS['get_type'] = MaplePtr('x -> disassemble(addressof(x))[1]')
MaplePtr.OBJECTS['whattype'] = MaplePtr('whattype')

def bitrepr(n, word=None):
    '''Binary string representation of integer n'''
    if n is None:
        return None
    elif n < 0:
        return '-' + bitrepr(-n)
    else:
        Q = []
        x = n
        while x >= 1:
            Q.append(str(x % 2))
            x /= 2
        Q.reverse()
        ret = ''.join(Q)
        if word is not None:
            return '0' * (word - len(ret)) + ret
        else:
            if n == 0: return '0'
            else: return ret 
        
#------------------------------------------------------------------------------#
#    Maple types to python
#------------------------------------------------------------------------------#                
def ctype(cmd):
    """Return the integer representation of the type assigned to the Maple 
    command cmd"""
    
    return MaplePtr(cmd).type()
    
AND = ctype('x and y')
CATENATE = ctype("'x||y'")
COMPLEX = ctype('I')
EQUATION = ctype('x = y')
EXPSEQ = ctype('op([x, y])')
FLOAT = ctype('1.0')
FUNCTION = ctype('y(x)')
IMPLIES = ctype('x implies y')
INEQUAT = ctype('x <> y')
INTNEG = ctype('-1')
INTPOS = ctype('1')
LESSEQ = ctype('x >= y')
LESSTHAN = ctype('x > y')
LIST = ctype('[x, y]')
MODULE = ctype('eval(LinearAlgebra)')
NAME = ctype('x')
NOT = ctype('not x')
OR = ctype('x or y')
POWER = ctype('x**y')
PROC = ctype('x -> x')
PROD = ctype('x**2')
RANGE = ctype('0..1')
RATIONAL = ctype('1/2')
RTABLE = ctype('rtable()')
SERIES = ctype('series(exp(x), x)')
SET = ctype('{x, y}')
STRING = ctype('"x"')
SUM = ctype('x+y')
TABLE = ctype('table()')
TABLEREF = ctype('x[y]')
UNEVAL = ctype("''x''")
XOR = ctype('x xor y')
ZPPOLY = ctype('modp1(ConvertIn(x,x),2)')
