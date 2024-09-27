#!/usr/bin/env python

from os.path import exists
from setuptools import setup
import versioneer

setup(name='toolz',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='List processing tools and functional utilities',
      url='https://github.com/pytoolz/toolz/',
      author='https://raw.github.com/pytoolz/toolz/master/AUTHORS.md',
      maintainer='Erik Welch',
      maintainer_email='erik.n.welch@gmail.com',
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
      python_requires=">=3.8",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "Programming Language :: Python :: 3.12",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy"])
