from maple.core import maple as _maple

# trigonometric and hyperbolic functions
sin = _maple.sin
cos = _maple.cos
tan = _maple.tan
sec = _maple.sec
csc = _maple.csc
cot = _maple.cot
sinh = _maple.sinh
cosh = _maple.cosh
tanh = _maple.tanh
sech = _maple.sech
csch = _maple.csch
coth = _maple.coth

# inverse trigonometric and hyperbolic functions
arcsin = _maple.arcsin
arccos = _maple.arccos
arctan = _maple.arctan
arcsec = _maple.arcsec
arccsc = _maple.arccsc
arccot = _maple.arccot
arcsinh = _maple.arcsinh
arccosh = _maple.arccosh
arctanh = _maple.arctanh
arcsech = _maple.arcsech
arccsch = _maple.arccsch
arccoth = _maple.arccoth

# a sample of the most useful/common mathematical functions
abs = _maple.abs
"""absolute value of real or complex number"""

argument = _maple.argument
"""argument of a complex number"""

bernoulli = _maple.bernoulli
"""Bernoulli numbers and polynomials"""

binomial = _maple.binomial
"""binomial coefficients"""

ceil = _maple.ceil
"""smallest integer greater than or equal to a number"""

dilog = _maple.dilog
"""dilogarithm function"""

csgn = _maple.csgn
"""complex ``half-plane'' signum function"""

erf = _maple.erf
"""error function"""

erfc = _maple.erfc
"""complementary error function and its iterated integrals"""

erfi = _maple.erfi
"""imaginary error function"""

euler = _maple.euler
"""Euler numbers and polynomials"""

exp = _maple.exp
"""exponential function"""

factorial = _maple.factorial
"""factorial function"""

floor = _maple.floor
"""greatest integer less than or equal to a number"""

frac = _maple.frac
"""fractional part of a number"""

harmonic = _maple.harmonic
"""partial sum of the harmonic series"""

hypergeom = _maple.hypergeom
"""generalized hypergeometric function"""

ilog2 = _maple.ilog2
"""ilog2"""

ilog10 = _maple.ilog10
"""ilog10"""

ilog = _maple.ilog
"""integer logarithms"""

ln = _maple.ln
"""natural logarithm (logarithm with base exp(1) = 2.71...)"""

lnGAMMA = _maple.lnGAMMA
"""log-Gamma function"""

log = _maple.log
"""logarithm to arbitrary base"""

log10 = _maple.log10
"""log to the base 10"""

max = _maple.max
"""max"""

min = _maple.min
"""maximum/minimum of a sequence of real values"""

pochhammer = _maple.pochhammer
"""pochhammer symbol"""

polar = _maple.polar
"""polar representation of complex numbers"""

polylog = _maple.polylog
"""polylogarithm function"""

round = _maple.round
"""nearest integer to a number"""

signum = _maple.signum
"""sign of a real or complex number"""

sqrt = _maple.sqrt
"""square root"""

surd = _maple.surd
"""non-principal root function"""

trunc = _maple.trunc
"""nearest integer to a number in the direction of 0"""

unwindK = _maple.unwindK
"""unwinding number"""

# already implemented as attributes of Algebraic instances
conjugate = _maple.conjugate
"""conjugate of a complex number or expression"""

Im = _maple.Im
"""imaginary part of a complex number"""

Re = _maple.Re
"""real part of a complex number"""