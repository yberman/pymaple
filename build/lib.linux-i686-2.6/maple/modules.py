from core import Maple, Proxy
from kernel import maple_help
import config
import types
import sys

class MapleLib(object):
    def __init__(self):
        self.blacklist = config.PY_BLACKLIST
        self.maple_blacklist = config.MAPLE_BLACKLIST
        
    def all(self):
        '''Return a list with all Maple function names'''
        
        funcs = maple_help('index[functions]')
        funcs = [ l.strip() for l in funcs.split('\n') if l.startswith('    ')]
        funcs = [ l for l in funcs if l ]
        ret = set()
        for l in funcs:
            ret = ret.union(l.split())
        
        ret.discard('_seed') # deprecated constant, raises an error    
        return list(ret.union(self.constants())) 
    
    def constants(self):
        '''Return a list of all Maple constants'''
        
        return 'Catalan constants Digits FAIL gamma I infinity lasterror libname Order Pi printlevel undefined'.split()
    
    def special(self):
        '''Return a list with all special functions'''
        
        return [ x for x in self.functions() if x[0].isupper() ]
    
    def functions(self):
        '''Return a list with all Maple functions'''
        
        return [ str(x) for x in Maple('FunctionAdvisor(known_functions, quiet)') ]
    
    def math(self):
        '''Return a list with all Maple functions not labeled as special'''
        
        math = set(self.functions()) - set(self.special())
        return list(math)
    
    def programming(self):
        '''Return a list with all programming related functions'''
        
        return 'addressof assemble comment DEBUG disassemble indexfcn keyword lasterror macro maplemint mint pointto profile rtable indexfcn showstat showstop stopat stoperror stoplast stopwhen trace tracelast traperror unprofile unstopat unstoperror unstopwhen untrace where'.split()
    
    def packages(self):
        raise NotImplementedError
    
    def py_name(self, func):
        '''Return a valid python name to function func'''
        
        if not func.isalnum:
            return None
        elif func in self.maple_blacklist:
            return None
        elif func in self.blacklist:
            return func + '_'
        else:
            return func

    def module(self, name, funcs, base='maple', cls=Maple):
        '''Makes a module 'name' using all functions in funcs'''
        
        mod = types.ModuleType(name)
        for f in funcs:
            fname = self.py_name(f)
            if fname:
                setattr(mod, f, cls(fname))
            
        mod_name = base + '.' + name
        sys.modules.setdefault(mod_name, mod)
        return mod

fl = MapleLib()
special = fl.module('special', fl.special())
programming = fl.module('programming', fl.programming())
constants = fl.module('constants', fl.constants())
math = fl.module('math', fl.math())
lib = fl.module('lib', fl.all())

__all__ = ['special', 'math', 'programming', 'constants', 'lib'] 