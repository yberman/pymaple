import sys
import StringIO

def std_grab(func, *args, **kwds):
    """Executes func(*args, **kwds) and returns the messages thown into the 
    standard output. 
    """
    return std_grab2(func, *args, **kwds)[1]
    
def std_grab2(func, *args, **kwds):
    """Similar to std_grab(), but it returns (res, stdout), where res is the 
    return value of func(*args, **kwds) and stdout is a string holding the 
    output.
    """
    
    old_out = sys.stdout
    sys.stdout = new_out = StringIO.StringIO()
    try:
        res = func(*args, **kwds)
    finally:
        sys.stdout = old_out
    st = new_out.getvalue()
    new_out.close()
    
    return (res, st)
