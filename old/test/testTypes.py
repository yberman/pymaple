from maple.symbolic.basic import *
import unittest
import sys
stdout = lambda x: sys.stdout.write(str(x) + ', ')

class TestBasicOP(unittest.TestCase):
    def setUp(self):
        self.x, self.y, self.z = symbol(*'xyz')
        self.half, self.two = Rational(1, 2), Rational(2)
        
    def testAddWorks(self):
        '''x + x == 2*x'''
        x, two = self.x, self.two
        
        print 'Equal values: ' 
        stdout(x + x)
        stdout(2 * x)
        stdout(x * 2)
        stdout(x * two)
        stdout(Prod(x, 2))
        stdout(Prod(x, two))
        
unittest.main(argv=['-v'])