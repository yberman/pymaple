from unittest import *
from maple import *

# Test basic operations
one, two, tree = maple(1), maple(2), maple(3)
x, y, z = lib.x, lib.y, lib.z

print 'Testing multiplication'
print x * y * z
print x * two
print x * 2
print x * 2L
print x * 2.
print 2 * x
print 2L * x
print 2. * x

print '\nTesting division'
print x / y
print x / two
print x / 2
print x / 2L
print x / 2.
print two / x
print 2 / x
print 2L / x
print 2. / x

print '\nTesting pow'
print x**y
print x**two
print x**2
print x**2L
print x**2.
print two**x
print 2**x
print 2L**x
print 2.**x

print '\nTesting alternate pow (fixme)'
print pow(x, y)
print pow(x, y, 1)
print pow(x, 2, 2)
print pow(two, x, y) #FIXME: right behaviour to pow

print '\nTesting sum'
print x + y
print x + two
print x + 2
print x + 2L
print x + 2.
print two + x
print 2 + x
print 2L + x
print 2. + x

print '\nTesting subtraction'
print x - y
print x - two
print x - 2
print x - 2L
print x - 2.
print two - x
print 2 - x
print 2L - x
print 2. - x