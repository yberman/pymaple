from kernel import maple, helpstr
from sys import modules
import imp

# invalid python names (or conflicting with builtins)
blacklist = 'and del from not while as elif global or with assert else if pass yield break except import print class exec in raise continue finally is return def for lambda try'.split()
blacklist += __builtins__.keys()

def maple_module(name, funcs):
    """Makes a Python module with all Maple funcs given in funcs"""
    #TODO: make delayed imports
    mod = imp.new_module(name)
    for f in funcs: 
        try:
            if f in blacklist:
                setattr(mod, f + '_', maple(f))
            else:
                setattr(mod, f, maple(f))
        except Exception, e:
            pass
        
    modules.setdefault('maple_%s' % name, mod)
    return mod

# math and special functions
functions = dict( (str(x), x) for x in maple('FunctionAdvisor(known_functions, quiet)') )
special_funcs = set(filter(lambda x: x[0].isupper(), functions.keys() ))
math_funcs = set(functions) - special_funcs

# maple constants
constants_names = \
'Catalan constants Digits FAIL gamma I infinity lasterror libname Order Pi printlevel undefined'.split()

# maple functions (this list is from index[functions])
help_page = helpstr('index[functions]')

fist_function = 'AiryAi' # remove the "Description" and "See Also" sections
head, sep, body = help_page.partition(fist_function)
body, sep, foot = body.partition('See Also')

other_funcs = set(body.replace('\n', '').split() + [ fist_function ])
other_funcs -= special_funcs | math_funcs | set(constants_names) | set(['_seed'])

# expressions
mod = imp.new_module('expressions')

# misc
mod.modop = maple('`mod`')
mod.fatop = maple('`!`')
mod.dollarop = maple('`$`')
mod.ditto1 = maple('`%`')
mod.ditto2 = maple('`%%`')
mod.ditto3 = maple('`%%%`')
mod.atop = maple('`@`')
mod.atatop = maple('`@@`')
mod.neutralop = maple('`&`')
mod.neutral = lambda x: maple('`&%s`' % x)
mod.setop = maple('`{}`')
mod.listlop = maple('`[]`')
mod.catop = maple('`||`')

# arithmetic
mod.mulop = maple('`*`')
mod.addop = maple('`+`')
mod.subop = maple('`-`')
mod.dotop = maple('`.`')
mod.divop = maple('`/`')
mod.powop = maple('`**`')
mod.hatop = maple('`^`')

# relations
mod.ltop = maple('`<`')
mod.leop = maple('`<=`')
mod.neop = maple('`<>`')
mod.neop = maple('`<>`')
mod.eqop = maple('`=`')
mod.gtop = maple('`>`')
mod.geop = maple('`>=`')

# logical
mod.andop = maple('`and`')
mod.orop = maple('`or`')
mod.xorop = maple('`xor`')
mod.impliesop = maple('`implies`')
mod.notop = maple('`not`')

# set
mod.unionop = maple('`union`')
mod.intersectop = maple('`intersect`')
mod.minusop = maple('`minus`')
mod.subsetop = maple('`subset`')

expressions = dict( (x, getattr(mod, x)) for x in dir(mod) if not x.startswith('_') )
modules.setdefault('maple_expressions', mod)

# programming
programming_funcs = 'comment DEBUG indexfcn keyword lasterror macro maplemint mint profile rtable indexfcn showstat showstop stopat stoperror stoplast stopwhen trace tracelast traperror unprofile unstopat unstoperror unstopwhen untrace where'.split()

# create modules
math_mod = maple_module('math', math_funcs)
special_mod = maple_module('special', special_funcs)
constants_mod = maple_module('constants', constants_names)
funcs_mod = maple_module('funcs', other_funcs)
programming_mod = maple_module('programming', programming_funcs)

# create lib module
mod = imp.new_module('lib')
dic = {}
for mod in [expressions, math_mod, special_mod, constants_mod, funcs_mod, programming_mod]: 
    dic.update(dict( (x, getattr(mod, x)) for x in dir(mod) if not x.startswith('_') ))
for k, v in dic.items():
    setattr(mod, k, v)
modules.setdefault('maple_lib', mod)

# import modules
import maple_math as math
import maple_special as special
import maple_constants as constants
import maple_programming as programming
import maple_expressions as expressions
import maple_lib as lib

__all__ = 'math special constants lib expressions programming'.split()
