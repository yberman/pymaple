#-*- coding: utf8 -*- 
from distutils.core import setup
from distutils.extension import Extension
import os
import sys

# we'd better have Cython installed, or it's a no-go
try:
    from Cython.Distutils import build_ext
except:
    print "You don't seem to have Cython installed. Please get a"
    print "copy from www.cython.org and install it"
    sys.exit(1)

# Define some variables
maple_path = '/home/chips/.bin/maple10' #TODO: do not hardcode this!
maple_lib_path = os.path.join(maple_path, 'bin.IBM_INTEL_LINUX')
os.environ['MAPLE'] = maple_path
os.environ['LD_LIBRARY_PATH'] = maple_lib_path

# Package variables 
package_name = 'maple'
package_dir = 'src/maple'
include_dir = os.path.join(maple_path, 'extern', 'include')
lib_dir = os.environ['LD_LIBRARY_PATH']
lib_gcc = [ 'maplec' ]

# scan directory for extension files, converting
# them to extension names in dotted notation
def scandir(dir, files=[]):
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if os.path.isfile(path) and path.endswith(".pyx"):
            files.append(path.replace(os.path.sep, ".")[:-4])
        elif os.path.isdir(path):
            scandir(path, files)
    return files

# generate an Extension object from its dotted name
def makeExtension(extName):
    extPath = extName.replace(".", os.path.sep)+".pyx"
    print extName, extPath, extName[len(package_dir) + 1:]
    return Extension(
        extName[len(package_dir) + 1:],
        [extPath],
        extra_compile_args = ["-O3" ], #, "-Wall"],
        extra_link_args = ['-g', '-L%s' % maple_lib_path],
        include_dirs = [ include_dir, '.' ], # adding the '.' to include_dirs is CRUCIAL!!
        library_dirs = [ lib_dir ], 
        libraries = lib_gcc,
        )

# get the list of extensions
extNames = scandir(package_dir)

# and build up the set of Extension objects
extensions = [ makeExtension(name) for name in extNames ]

# finally, we can pass all this to distutils
setup(
  # meta info
  name = package_name, 
  version = '0.1',
  url = 'http://code.google.com/p/pymaple',
  author = 'Fábio Macêdo Mendes',
  author_email = 'fabiomacedomendes@gmail.com',
  description = "Python bindings for Maple runtime.",
  long_description = """\
  Maple has an extensive library of symbolic computation routines. This 
  project aims to make all Maple functions available to Python and to 
  provide a more convinient interface to these libraries. 

  The bindings use the OpenMaple C interface. 
  """,
  classifiers = [
    "Development Status :: 3 - Alpha/Planning",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GPL",
    "Operating System :: Linux",
    "Programming Language :: Python",
    "Programming Language :: Cython",
    "Topic :: Software Development :: Symbolic computing", #???
    "Topic :: Software Development :: Libraries :: Python Modules"
  ],

  # building info
  cmdclass = {'build_ext': build_ext},
  ext_package='maple',
  ext_modules = extensions,
  packages=[package_name],
  package_dir = { 'maple': package_dir},
  )
