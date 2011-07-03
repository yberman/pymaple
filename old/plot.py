from mtypes import *
from kernel import maple
import pylab

def to_mplot(plot):
    """Convert Maple plot to Matplotlib.
    
    It is necessary to call pylab.show(), pylab.save() or similar to 
    actually render the plot.
    """
    #TODO: document it better
    
    try:
        if not str(plot.operator) == 'PLOT':
            raise TypeError
    except:
        raise TypeError('Invalid plot "%s"' % plot)
    
    for op in plot.operands:
        name = str(op.operator)
        if name == 'CURVES':
            #TODO: support for color
            data, color = op.operands
            X = [ float(x[0]) for x in data ]
            Y = [ float(x[1]) for x in data ]
            pylab.plot(X, Y)  
        elif name == 'AXESLABELS':
            lx, ly = op.operands
            pylab.xlabel(lx)
            pylab.ylabel(ly)
        elif name == 'TITLE':
            pylab.title('title')
        elif name == 'VIEW':
            #TODO: support view
            pass
        else:
            print 'dbg: unexpected plot argument %s' % op

def mplot(*args, **kwds):
    """Call Maple plot function and convert the output to a Matplotlib plot.
    
    This function returns the pylab module so the following idiom works
    
    >>> p = mplot(x**2, x)
    >>> p.show() # displays the plot
    >>> print p.__name__
    pylab
    
    """
    
    to_mplot(maple('plot')(*args, **kwds))
    return pylab


__all__ = [ 'mplot' ]
