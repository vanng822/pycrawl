
import os

from setuptools import setup, find_packages

from distutils.core import Extension
 
#dateutil = Extension('dateutil', sources = ['src/module/dateutil.c'])
fib = Extension('fib', sources = ['src/module/fib.c'])


here = os.path.abspath(os.path.dirname(__file__))


requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'sqlalchemy',
    'couchdb',
    'psycopg2',
    'waitress',
    ]

setup(name='pycrawl',
      version='0.1',
      author='',
      author_email='',
      url='',
      packages=find_packages(),
      test_suite="tests",    
      ext_modules = [fib],                      
)