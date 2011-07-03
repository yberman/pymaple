from unittest import TestCase, main
from maple import *

x, y, z = map(maple, 'xyz')
f, g, h = map(maple, 'fgh')

class MapleObject(TestCase):
    def test_print(self):
        """print objects work"""
        assert str(x) == 'x' 
        
    def test_call(self):
        """call maple objects"""
        assert h() == maple('h()')
        assert f(x) == maple('f(x)')
        assert h(x, y=z) == maple('h(x,y=z)')
        assert h(x, y=z) == h(x, y==z)
        
    def test_call_numeric(self):
        """call python numeric objects"""
        assert f(1) == maple('f(1)')
        assert f(1.) == maple('f(1.)')
        assert f(2j) == maple('f(2.*I)')
        assert f(2.j) == maple('f(2.*I)')
        assert f(complex(1)) == maple('f(1.)')
        assert f(1L) == maple('f(1)')
        
    def test_call_string(self):
        """call python strings"""
        assert f('st') == maple('f("st")')
    
    def test_call_containers(self):
        """call python containers"""
        assert f((x, y)) == maple('f(x,y)')
        assert f([x, y]) == maple('f([x,y])')
        assert f(set([x, y])) == maple('f({x,y})')
        
    def test_arithmetic(self):
        """arithmetic operations"""
        assert x + y == maple('x + y')
        assert x - y == maple('x - y')
        assert x * y == maple('x * y')
        assert x / y == maple('x / y')
        assert x ** y == maple('x ** y')
        assert -x == maple('-x')
        
        
    def test_numeric_cast(self):
        """casting operations"""
        self.assertAlmostEqual(float(maple('1.0')), 1.0)
        assert int(maple('1')) == 1
        assert int(maple('1.0')) == 1
        assert long(maple('1.0')) == 1L
        assert type(long(maple('1.0'))) == long
        assert (maple('1') == maple('1')) and True
        assert (not (maple('1') == maple('2'))) and True
    
    
class MapleTypes(TestCase):   
    def test_Name(self):
        """Name type"""
        assert Name('x') == maple('x')
        assert type(Name('x')) == Name
        assert Name(x) == Name('x')
        
    def test_Function(self):
        """Name type"""
        assert Function('f', x) == maple('f(x)')
        assert Function(f, x) == maple('f(x)')
        assert Function('int', x, x) == maple('x**2/2')
        assert type(Function(f, x)) == Function
        
    def test_Procedure(self):
        """Name type"""
        assert Procedure(f(x), x) == maple('x -> f(x)')
        #assert Procedure(f(x)) == maple('x -> f(x)') # unamed unapply
        assert type(Procedure(f(x), x)) == Procedure
        
    def test_Numeric(self):
        """select correct Numeric types"""
        assert type(maple('1')) == Integer
        assert type(maple('1/2')) == Rational
        assert type(maple('1*I')) == Complex
        assert type(maple('1.0')) == Float

    def test_Relation(self):
        """select correct Relation types"""
        assert type(maple('x = y')) == RelEQ
        assert type(maple('x <> y')) == RelNE
        assert type(maple('x < y')) == RelLT
        assert type(maple('x <= y')) == RelLE

    def test_Logical(self):
        """select correct Logical types"""
        assert type(maple('not x')) == NOT
        assert type(maple('x or y')) == OR
        assert type(maple('x xor y')) == XOR
        assert type(maple('x and y')) == AND
        assert type(maple('x implies y')) == IMPLIES

        
class MapleFunctions(TestCase):
    def test_help(self):
        """help system"""
        assert isinstance(helpstr('int'), basestring)
        assert helpstr('int') > 10
        assert helpstr(lib.int_) > 10
        
    def test_wrong_int(self):
        """test random functions"""
        self.assertRaises(TypeError, lib.int_, x)
        self.assertRaises(SyntaxError, maple, 'int(x')
        
        
if __name__ == '__main__':    
    main()
