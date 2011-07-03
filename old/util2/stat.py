from scipy import *
from util import assure
import random
__rand = random.random

def roulette(prob, norm=None):
    """Pick up an integer index with probability density 'prob'
    
    @param prob: array with probability density function
    """
    
    # run some checks
    assert isinstance(prob, ArrayType), 'Only works with arrays'
    assert (prob >=0).all(), 'Negative probabilities: %s' % str(prob)
    
    if norm is None:
        norm = prob.sum()
        assert norm > 0 or isinf(norm), 'Probabilities non-normalizable'
    
    # choose a number
    r = __rand() * norm
    
    pie_size = 0
    for idx, x in enumerate(prob):
        pie_size += x
        if r < pie_size:
            return idx
    assert False, 'Internal logic error'
