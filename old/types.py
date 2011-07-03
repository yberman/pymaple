from kernel import maple, Maple, register

#------------------------------------------------------------------------------
#    BASE TYPES
#------------------------------------------------------------------------------
__conjugate__ = maple('conjugate')
__imag__ = maple('Im')
__real__ = maple('Re')
class Algebraic(Maple):
    @property
    def conjugate(self): return __conjugate__(self)
        
    @property
    def imag(self): return __imag__(self)
        
    @property
    def real(self): return __real__(self)

__op__ = maple('op')
class Composite(Maple):
    @property
    def operands(self): return __op__(self)
    
    @property
    def operator(self): return __op__(0, self)

class Expression(Algebraic):
    pass

class Name(Expression):
    def __new__(cls, name):
        """Name represents an unknown.
        
        Input
        -----
        
        @name: a string
        
        """
        
        if '`' in str(name):
            raise ValueError('Invalid name "%s"' % name)
        return maple('`%s`' % name)

class Function(Composite, Expression):
    def __new__(cls, name, *args, **kwds):
        """Function(name, *args) <==> Name(name)(*args)"""
        
        return Name(name)(*args, **kwds)

class Procedure(Composite, Expression):
    def __new__(cls, expr, *args):
        """Procedure(expr, args) <==> unapply(expr, *args)"""
        #TODO: make python functions be passable as argument
        return maple('unapply')(expr, *args)

#------------------------------------------------------------------------------
#    NUMERIC TYPES
#------------------------------------------------------------------------------
class Numeric(Expression):
    pass

class Integer(Numeric):
    def __new__(self, i):
        """Integer(x) <==> trunc(x)"""
        return maple('trunc')(i)

class Rational(Numeric):
    numer = property(maple('numer'))
    denom = property(maple('denom'))
    
    def __new__(cls, numer, denom=1):
        """Implements fraction arithmetic and arbitrary precision integers.
        Denominator and numerator can also be accessed from the X.numer and
        X.denom attributes.
        
        Attributes and Input
        --------------------
        
        @numer: python or maple integer representing numerator
        @denom: python or maple integer representing denominator
        
        Observations
        ------------
        
        The constructor works identically as  frac(numer, denom).
        """
        
        return maple('frac')(numer, denom)

class Complex(Numeric):
    def __new__(cls, re, im):
        """Creates a complex number with real part equal to re and imaginary
        part im."""
        
        return maple('Complex')(re, im)

class Float(Numeric):
    def __new__(self, fp):
        """Float(x) <==> evalf(x)"""
        return maple('evalf')(fp)

#------------------------------------------------------------------------------
#    RELATION TYPES
#------------------------------------------------------------------------------
class Binary(Composite):
    lhs = property(maple('lhs'))
    rhs = property(maple('rhs'))

class Relation(Binary):
    pass

class RelEQ(Relation):
    def __new__(self, x, y):
        return x == y

class RelNE(Relation):
    def __new__(self, x, y):
        return x != y

class RelLT(Relation):
    def __new__(self, x, y):
        return x < y

class RelLE(Relation):
    def __new__(self, x, y):
        return x <= y

#------------------------------------------------------------------------------
#        LOGICAL OPERATORS
#------------------------------------------------------------------------------
class Logical(Algebraic, Composite):
    """Implements Boolean expressions"""
    pass

class NOT(Logical):
    def __new__(self, obj):
        """Logical not to object obj"""
        return maple('`not`')(obj)
 
class OR(Logical, Binary):
    def __new__(self, obj1, obj2):
        """Logical OR between obj1 and obj2"""
        return maple('`or`')(obj1, obj2)

class XOR(Logical, Binary):
    def __new__(self, obj1, obj2):
        """Logical XOR between obj1 and obj2"""
        return maple('`xor`')(obj1, obj2)

class AND(Logical, Binary):
    def __init__(self, obj1, obj2):
        """Logical AND between obj1 and obj2"""
        return maple('`and`')(obj1, obj2)

class IMPLIES(Logical, Binary):
    def __init__(self, obj1, obj2):
        """Logical implication between obj1 and obj2 (obj1 => obj2)"""
        return maple('`implies`')(obj1, obj2)

#------------------------------------------------------------------------------
#    COMPOSITE EXPRESSION TYPES
#------------------------------------------------------------------------------
class Prod(Expression, Composite):
    def __new__(cls, *args):
        """Prod(x1, x2, ..., xn) <==> x1 * x2 * ... * xn."""
        
        return maple('`*`')(*args)

class Add(Expression, Composite):
    def __new__(cls, *args):
        """Add(x1, x2, ..., xn) <==> x1 + x2 + ... + xn."""
        
        return maple('`+`')(*args)

class Pow(Expression, Composite):
    def __new__(cls, num, exp):
        """Pow(a, b) <==> a**b"""
        
        return num**exp

#------------------------------------------------------------------------------
#        SEQUENCES OBJECTS (separate hierachy?)
#------------------------------------------------------------------------------
 
class Sequence(Algebraic): pass
class array(Sequence): pass
class Array(Sequence): pass
class Matrix(Sequence): pass
class Set(Sequence): pass
class Table(Sequence): pass
class Hfarray(Sequence): pass
class Indexed(Sequence): pass
class List(Sequence): pass
class VectorColumn(Sequence): pass
class VectorRow(Sequence): pass

#------------------------------------------------------------------------------
#        SERIES TYPES
#------------------------------------------------------------------------------

# Expression types
class SeriesType(Expression, Composite): pass
class Series(SeriesType): pass
class Zppoly(SeriesType): pass
class SDMPolynom(SeriesType): pass

#------------------------------------------------------------------------------
#        MISCELANEOUS OBJECTS
#------------------------------------------------------------------------------
  
class Uneval(Algebraic): pass
class Range(Algebraic): pass
class Type(Algebraic): pass
class Concat(Algebraic): pass

#------------------------------------------------------------------------------
#        MODULES
#------------------------------------------------------------------------------
  
class Module(Maple): pass

#-----------------------------------------------------------------------------#
#    LINEAR ALGEBRA
#-----------------------------------------------------------------------------#

# Funcs in LinearAlgebra package
# `&x`, Add, Adjoint, BackwardSubstitute, BandMatrix, Basis, BezoutMatrix,
# BidiagonalForm, BilinearForm, CharacteristicMatrix, CharacteristicPolynomial,
# Column, ColumnDimension, ColumnOperation, ColumnSpace, CompanionMatrix,
# ConditionNumber, ConstantMatrix, ConstantVector, Copy, CreatePermutation,
# CrossProduct, DeleteColumn, DeleteRow, Determinant, Diagonal, DiagonalMatrix,
# Dimensions, DotProduct, EigenConditionNumbers, Eigenvalues,
# Eigenvectors, Equal, ForwardSubstitute, FrobeniusForm, GaussianElimination,
# GenerateEquations, GenerateMatrix, GetResultDataType, GetResultShape,
# GivensRotationMatrix, GramSchmidt, HankelMatrix, HermiteForm,
# HermitianTranspose, HessenbergForm, HilbertMatrix, HouseholderMatrix,
# IdentityMatrix, IntersectionBasis, IsDefinite, IsOrthogonal, IsSimilar,
# IsUnitary, JordanBlockMatrix, JordanForm, LA_Main, LUDecomposition,
# LeastSquares, LinearSolve, Map, Map2, MatrixAdd, MatrixExponential,
# MatrixFunction, MatrixInverse, MatrixMatrixMultiply, MatrixNorm,
# MatrixPower, MatrixScalarMultiply, MinimalPolynomial,
# Minor, Modular, Multiply, NoUserValue, Norm, Normalize, NullSpace,
# OuterProductMatrix, Permanent, Pivot, PopovForm, QRDecomposition,
# RandomMatrix, RandomVector, Rank, RationalCanonicalForm,
# ReducedRowEchelonForm, Row, RowDimension, RowOperation, RowSpace,
# ScalarMatrix, ScalarMultiply, ScalarVector, SchurForm, SingularValues,
# SmithForm, SubMatrix, SubVector, SumBasis, SylvesterMatrix, ToeplitzMatrix,
# Trace, Transpose, TridiagonalForm, UnitVector, VandermondeMatrix,
# VectorAdd, VectorAngle, VectorMatrixMultiply, VectorNorm,
# VectorScalarMultiply, ZeroMatrix, ZeroVector, Zip

class LinearAlgebra(Composite):
    transpose = property(maple('LinearAlgebra:-Transpose'))
    htranspose = property(maple('LinearAlgebra:-HermitianTranspose'))
    norm = property(maple('LinearAlgebra:-Norm'))
    dim = property(maple('LinearAlgebra:-Dimension'))
    readonly = property(maple('readonly')) #??
    
    def __hash__(self):
        if not self.readonly:
            raise TypeError('Mutable Matrices cannot be hashed')
        else:
            return Composite.__hash__(self)
    
    def __len__(self):
        return self.dim
    
    def __mul__(self, other):
        if isinstance(other, LinearAlgebra):
            # non comutative mul
            #TODO: check valid multiplications between Matrices and Vectors
            return maple('`.`')(self, other)
        else:
            return Composite.__mul__(self, other)

class Vector(LinearAlgebra):
    def __init__(self, *args, **kwds):
        """Construct a Vector object
        
        Calling sequences
        -----------------
        
        Vector(dim, [rule, ], **kwds)
            
            Return a dim-dimensinal vector filled with zeros. If the optional
            rule argument is given, the function rule(i) is called for each
             vector element. Vector[i]. Optional keywords arguments are described
            bellow.
        
        Vector(iter, **kwds)
             
             Return a vector whose elements inherit from an iterable iter.
            Optional keywords arguments are described bellow.
        
        
        Keyword Arguments (not supported yet)
        -----------------
         
         @parm is_row: (boolean) if True, returns a column vector, otherwise,
                returns a column vector.
        
        @param readonly: (boolean) specify whether Vector entries can be changed
        
        @param symbol: (Symbol) symbolic name to be used for Vector entries
         
        @param scan:(Symbol or iterable) specify the structure and/or data
                 order for interpreting initial values; interpreter for initial
                values in parameter iterable
         
        @parm shape: (Symbol or iterable) specify one or more built-in or
                 user-defined indexing functions; storage allocation for
                Vector entries
        
        @param storage: (string) permitted storage mode; storage
                requirements for Vector entries
        
        @param datatype: (any Maple type); type of data stored in Vector
         
        @param fill: value is of the type specified by the datatype parameter;
                specifies Vector entries at locations not otherwise set
         
        @param attributes: (iterable) specifies permitted attributes;
                specifies additional mathematical properties of the Vector
                
        
        Observations
        ------------
        
        All container types in Maple are indexed starting with one, differently
        to python where indexing starts with zero. We follow python's
        convention here.
        
        Differently to Maple implementation, both column and row vectors are
        the same type here. Test for the is_col and is_row attributes to check
        a given Vector orientation.
        
        Attributes
        ----------
        
        @param is_col: True for a column vector, False otherwise
        @param is_row: True for a row vector, False otherwise
        """
        
        if len(args) > 2:
            raise ValueError('Wrong number of arguments')
        
        # col or row vectors
        if kwds.get('is_row', False):
            vector = self._vector_row
        else:
            vector = self._vector_col
        
        #TODO: support to all keyword args
        #self.readonly = kwds.get('readonly', False)
        #self.symbol = kwds['symbol']
        #self.scan = kwds['scan']
        #self.shape = kwds['shape']
        #self.storage = kwds['storage']
        #self.datatype = kwds['datatype']
        #self.fill = kwds['fill']
        #self.attributes = kwds['attributes']
        aqueue = [ args[0] ]
        try:
            func = args[1]
            aqueue.append([ func(i) for i in xrange(dim) ])
        except IndexError:
            pass
        
        self._from_dag(vector(*aqueue))

    @property
    def is_row(self):
        return 'row' in str(self._whattype, self)
    
    @property
    def is_col(self):
        return not self.is_row

class Matrix(LinearAlgebra):
    def __init__(self, *args, **kwds):
        """Construct a Matrix object
        
        Calling sequences
        -----------------
        
        Matrix(nrows, ncols, [ proc, ] **kwds)
            
            Builds a nrows x ncols matrix filled with zeros. If the optional
             proc is given, Matrix[i, j] elements are initialized as proc(i,j).
            Optional keyword arguments are described bellow.
        
        Matrix(init, **kwds)
             
             init may be iterable, another Matrix or a Vector. Optional keyword
            arguments are described bellow.
        
        Keyword arguments (not supported yet)
        -----------------
          
          @param readonly: (boolean) specify whether Matrix entries can be
                 changed
         
         @param symbol: (Symbol) symbolic name to be used for the Matrix entries
          
          @param scan:(Symbol or iterable) specify the structure and/or data
                  order for interpreting initial values; interpreter for initial
                 values in parameter init
          
          @parm shape: (Symbol or iterable) specify one or more built-in or
                  user-defined indexing functions; storage allocation for
                 Matrix entries
         
         @param name storage: (string) permitted storage mode; storage
                 requirements for Matrix entries
          
          @param order: (string) either C_order or Fortran_order; specifies
                 if Matrix entries are stored by rows or columns
         
         @param datatype: (any Maple type); type of data stored in Matrix
          
          @param fill: value is of the type specified by the datatype parameter;
                 specifies Matrix entries at locations not otherwise set
          
          @param attributes: (iterable) specifies permitted attributes;
                 specifies additional mathematical properties of the Matrix
        """
        
        if len(args) > 3:
            raise ValueError('Wrong number of arguments')
        
        #TODO: support to all keyword args
        #self.symbol = kwds['symbol']
        #self.scan = kwds['scan']
        #self.shape = kwds['shape']
        #self.storage = kwds['storage']
        #self.datatype = kwds['datatype']
        #self.fill = kwds['fill']
        #self.attributes = kwds['attributes']
        try:
            # first and second argument are integers
            dr, dc = int(args[0]), int(args[1])
            try:
                # function is defined
                func = args[2]
                data = [ [ func(i, j) for i in xrange(dr) ] for j in xrange(dc) ]
            except:
                # simple constructor
                data = None
                self._from_dag(self._matrix(dr, dc))
        except TypeError, ValueError:
            # first argument is data --- delay construction
            data = args[0]
        
        if not data is None:
            self._from_dag(self._matrix(list(data)))
    
    def determinant(self):
        pass
    
    def __len__(self):
        x, y = self.shape
        return x * y
    
    @property
    def shape(self):
        """M.shape -> (rows, cols)
        
        Tuple with the shape of a Matrix"""
        
        return LinearAlgebra.__len__(self)
    
    def __len__(self):
        """M.__len__() <==> len(M)"""
        r, c = self.shape
        return r * c


#------------------------------------------------------------------------------
# Register Python classes with the maple kernel
#------------------------------------------------------------------------------

# Base types
register('x', Name)
register('f(x)', Function)
register('x -> x', Procedure)

# Numeric types
register('1', Integer)
register('-1', Integer)
register('1/2', Rational)
register('1*I', Complex)
register('1.0', Float)

# Relation types
register('x < y', RelLT)
register('x <= y', RelLE)
register('x = y', RelEQ)
register('x <> y', RelNE)

# Logical types
register('not x', NOT)
register('x or y', OR)
register('x xor y', XOR)
register('x and y', AND)
register('x implies y', IMPLIES)

#...
#TODO: register all maple types

# only export proper maple types
__all__ = [ x for x in locals().values() if type(x) == type ]
__all__ = [ x.__name__ for x in __all__ if Maple in x.mro() ]