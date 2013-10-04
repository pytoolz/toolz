#!/usr/bin/env python

from os.path import exists
from setuptools import setup
import toolz

setup(name='toolz',
      version=toolz.__version__,
      description='List processing tools and functional utilities',
      url='http://github.com/pytoolz/toolz/',
      author='Matthew Rocklin',
      author_email='mrocklin@gmail.com',
      license='BSD',
      keywords='functional utility itertools functools',

      packages=['toolz',
                'toolz.itertoolz',
                'toolz.functoolz',
                'toolz.dicttoolz'],
      long_description=open('README.md').read() if exists("README.md") else "",
      zip_safe=False)
