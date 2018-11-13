#!/usr/bin/env python

from os.path import exists
from setuptools import setup
import toolz

setup(name='toolz',
      version=toolz.__version__,
      description='List processing tools and functional utilities',
      url='https://github.com/pytoolz/toolz/',
      author='https://raw.github.com/pytoolz/toolz/master/AUTHORS.md',
      maintainer='Matthew Rocklin',
      maintainer_email='mrocklin@gmail.com',
      license='BSD',
      keywords='functional utility itertools functools',
      packages=['toolz',
                'toolz.sandbox',
                'toolz.curried',
                'tlz'],
      package_data={'toolz': ['tests/*.py']},
      long_description=(open('README.rst').read() if exists('README.rst')
                        else ''),
      zip_safe=False,
      python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy"])
