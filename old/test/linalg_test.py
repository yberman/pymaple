from maple import *
from maple.lib import *
from maple.core.cmaple import cmaple
from maple.core import to_c

def test_convertion_to_iterables():
    x, y, z = symbol(*'xyz')
    repr = cmaple.repr
    print 'tuple of numbers', repr(to_c.iterable_to_c((1,2,3)))
    print 'tuple of DAGS', repr(to_c.iterable_to_c((x,y,z)))
    print 'generator of numbers', repr(to_c.iterable_to_c(xrange(10)))
    print '*** conversion to iterables passed***'
    
test_convertion_to_iterables()
    
def test_vector_calling_sequences():
    x, y, z = symbol(*'xyz')
    
    print 'Empty vector', Vector(3)
    print 'Vector', Vector([x,y,z])
    print 'Row vector', Vector([x,y,z], is_row=True)
    print 'Function generated', Vector(3, lambda n: x**n)
    print '*** vectors passed***'
    
test_vector_calling_sequences()