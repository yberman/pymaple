'''
Created on 31/10/2009

@author: chips
'''

# Constants
PY_BLACKLIST = ('and del from not while as elif global or with assert else if'
+ ' pass yield break except import print class exec in raise continue finally'
+ ' is return def for lambda try').split()
PY_BLACKLIST += dir(__builtins__)

MAPLE_BLACKLIST = 'assuming module tracelast'.split()
