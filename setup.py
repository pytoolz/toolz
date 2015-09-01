#!/usr/bin/env python

from os.path import exists
from setuptools import setup
import toolz

setup(name='toolz',
      version=toolz.__version__,
      description='List processing tools and functional utilities',
      url='http://github.com/pytoolz/toolz/',
      author='https://raw.github.com/pytoolz/toolz/master/AUTHORS.md',
      maintainer='Matthew Rocklin',
      maintainer_email='mrocklin@gmail.com',
      license='BSD',
      keywords='functional utility itertools functools',
      packages=['toolz',
                'toolz.sandbox',
                'toolz.curried'],
      package_data={'toolz': ['tests/*.py']},
      long_description=(open('README.rst').read() if exists('README.rst')
                        else ''),
      zip_safe=False)
