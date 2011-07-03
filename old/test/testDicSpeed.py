from random import *
from time import clock

print 'Ideally, acess time for dict keys should be constant. Let us test it'

def consume(iter):
    for i in iter:
        pass

dic1 = dict( (i, 2) for i in xrange(10) )
dic2 = dict( (i, 2) for i in xrange(1000) )
dic3 = dict( (i, 2) for i in xrange(1000000) )


keys1 = range(10)
keys2 = sample(range(1000), 100)
keys3 = sample(range(1000000), 500)

print 'Testing 1st dict: len=10'
t0 = clock()
for key in keys1:
    consume( dic1[key] for i in xrange(100000) )
print t0 - clock(), (t0 - clock()) / 10.

print
print 'Testing 1st dict2: len=1000'
t0 = clock()
for key in keys2:
    consume( dic2[key] for i in xrange(100000) )
print t0 - clock(), (t0 - clock()) / 100.

print
print 'Testing 1st dict: len=1000000'
t0 = clock()
for key in keys3:
    consume( dic3[key] for i in xrange(100000) )
print t0 - clock(), (t0 - clock()) / 500.

