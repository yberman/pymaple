from kernel import maple, Maple, mhelp, helpstr
from mtypes import *
from functions import *
from plot import *

# convenience variables
x, y, z, i, j, k = map(maple, 'xyzijk')
one, zero = maple('[1,0]')
oo = maple('infinity')

f = maple('[x,y,z]')
print f, type(f)