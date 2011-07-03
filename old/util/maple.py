import os
import re

#-----------------------------------------------------------------------------#
#
#    GET MAPLE SYSTEM VARIABLES
#
#-----------------------------------------------------------------------------#

def get_maple_system_type():
    """Returns the output of maple.system.type command"""
    
    stdin, out, err = os.popen3('maple.system.type')
    out, err = out.read(), err.read()
    if err:
        msg = 'Error trying to execute maple.system.type script: %s'
        raise OSError(msg % err)
    else:
        return out.replace('\n', '')
    
def get_maple_path():
    """Return the full path to libmaplec.so if it is not on LIBMAPLEC_PATH"""
    
    # Only supports Linux. I don't care about other OSes. If you care, 
    if not os.name == 'posix':
        raise RunTimeError, 'OS not supported. Use Linux/Unix instead' 

    # for linux
    try:
        return os.environ['MAPLE_PATH']
    except:
        # maple will be in one of these various paths
        mpaths = os.popen('whereis maple').read()[:-1].split(' ')[1:]
        regex = re.compile(r"MAPLE='(?:[\w/]+)'") # matches the entry MAPLE='<maple_path>' on maple start script
        
        mpath = ''
        for path in mpaths:
            # read a file and matches it
            f = file(path, 'r')
            data = list(f)
            for line in data:
                # try to match the line with maple_path
                if 'MAPLE' in line:
                    try:
                        mpath = regex.findall(line)[0]
                        mpath = mpath[:-1].split("'")[-1]
                        break
                    except IndexError:
                        pass           
            f.close()
        
        # fill the path up to libmaplec.so
        #arch = os.popen('maple.system.type').read().replace('\n', '')
        #mpath = os.path.join(mpath, arch)
            
        # asserts that path really exists
        if not os.path.exists(mpath):
            raise RuntimeError, 'Invalid path to Maple libs: %s\nYou should define it on MAPLE_PATH enviroment variable' % mpath
        
        # we're done!
        return mpath
    

class _foreign_initializer(object):
    def __new__(cls, c_obj, class_):
        """Creates a new instance of class_"""
        obj = object.__new__(class_)
        obj._as_parameter_ = c_obj._as_parameter_
        obj._id = c_obj._id
        obj._set_up()
        return obj
    
#TODO: probably this should go elsewhere
def new_py_object(c_obj, class_):
    """Initialize a python object of type class_ given which references 
    a corresponding maple c_obj"""
    return _foreign_initializer(c_obj, class_)