#!/usr/bin/env python

from os.path import exists
from setuptools import setup

setup(name='toolz',
      version='0.2.1',
      description='More tools',
      url='http://github.com/mrocklin/toolz',
      author='Matthew Rocklin',
      author_email='mrocklin@gmail.com',
      license='BSD',
      packages=['toolz'],
      long_description=open('README.md').read() if exists("README.md") else "",
      zip_safe=False)
