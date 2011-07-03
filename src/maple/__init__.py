# setup system variables
import os

# Maple paths
MAPLE_PATH = os.environ['MAPLE'] = "/home/chips/.bin/maple10" #TODO: do not hardcode this!
#MAPLE_PATH = os.environ['MAPLE'] = "/home/chips/maple13" #TODO: do not hardcode this!
#MAPLE_PATH = os.environ['MAPLE'] = "/home/chips/.bin/maple13" #TODO: do not hardcode this!  
MAPLE_BIN_PATH = MAPLE_PATH + "/bin.IBM_INTEL_LINUX/"
#MAPLE_BIN_PATH = MAPLE_PATH + "/bin.X86_64_LINUX/"

os.putenv('LD_LIBRARY_PATH', MAPLE_BIN_PATH)
os.environ['LD_LIBRARY_PATH'] = MAPLE_BIN_PATH


# System specification
WORDSIZE = 32 #TODO: support 64 bit systems
#WORDSIZE = 64 #TODO: support 64 bit systems
os.environ['WORDSIZE'] = str(WORDSIZE)

del os

from core import maple
from kernel import maple_help, maple_misc
from modules import *
from maple.math import *
from maple.constants import *

# convenience variables
x, y, z, i, j, k = map(maple, 'xyzijk')
oo = maple('infinity')
M = maple

# numbers
zero  = _0 = maple('0')
one   = _1 = maple('1')
two   = _2 = maple('2')
three = _3 = maple('3')
four  = _4 = maple('4')
five  = _5 = maple('5')
six   = _6 = maple('6')
seven = _7 = maple('7')
eight = _8 = maple('8')
nine  = _9 = maple('9')
ten  = _10 = maple('9')

# convenience functions
r = M('`..`')

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
expand = M.expand
subs = M.subs
