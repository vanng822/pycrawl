
import os

from setuptools import setup, find_packages

from distutils.core import Extension
from Cython.Distutils import build_ext

cmandelbrot = Extension('cmandelbrot', sources = ['src/module/cmandelbrot.c']) 
camlich = Extension('camlich', sources = ['src/module/camlich.c'])
fib = Extension('fib', sources = ['src/module/fib.c'])
dateutil = Extension('dateutil', sources = ['src/module/cdate_util.c'])

cyiterator = Extension('cyiterator', ['mandelbrot/iterator.pyx'])

gps_util = Extension('gps_util', ['gps_util/gps_util.pyx'])

here = os.path.abspath(os.path.dirname(__file__))


install_requires = [
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
      cmdclass = {'build_ext': build_ext},
      ext_modules = [gps_util, cmandelbrot, fib, camlich, dateutil, cyiterator],
)