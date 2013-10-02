#!/usr/bin/env python

from os.path import exists
from setuptools import setup

setup(name='toolz',
      version='0.2.2',
      description='More tools',
      url='http://github.com/pytoolz/toolz/',
      author='Matthew Rocklin',
      author_email='mrocklin@gmail.com',
      license='BSD',
      packages=['toolz',
                'toolz.itertoolz',
                'toolz.functoolz',
                'toolz.dicttoolz'],
      long_description=open('README.md').read() if exists("README.md") else "",
      zip_safe=False)
