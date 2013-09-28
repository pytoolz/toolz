Toolz
=====

A set of common utility functions for iterators, functions, and dictionaries.

[![Build Status](https://travis-ci.org/pytoolz/toolz.png)](https://travis-ci.org/pytoolz/toolz)


LICENSE
-------

New BSD.  See [License File](LICENSE.TXT).

Install
-------

`toolz` is on the Python Package Index (PyPi)

    pip install toolz

or 
    
    easy_install toolz

Structure and Heritage
----------------------

Toolz is implemented in three parts:

[`itertoolz`](https://github.com/pytoolz/toolz/blob/master/toolz/itertoolz/core.py), 
for opertions on iterables.  Examples: `groupby`, `unique`, `interpose`,

[`functoolz`](https://github.com/pytoolz/toolz/blob/master/toolz/functoolz/core.py),
for higher-order functions.  Examples: `memoize`, `curry`, `comp`

[`dicttoolz`](https://github.com/pytoolz/toolz/blob/master/toolz/dicttoolz/core.py),
for operations on dictionaries.  Examples: `assoc`, `update-in`, `merge`.

These functions come from the legacy of functional languages for list 
processing.  They interoperate well to accomplish common complex tasks.


Example
-------

This builds a standard wordcount function from pieces within `toolz`

>>> def stem(word):
...     """ Stem word to primitive form """
...     return word.lower().rstrip(",.!'")

>>> from toolz.curried import comp, frequencies, map
>>> wordcount = comp(frequencies, map(stem), str.split)

>>> sentence = "This cat jumped over this other cat!"
>>> wordcount(sentence)
{'this': 2, 'cat': 2, 'jumped': 1, 'over': 1, 'other': 1}


Dependencies
------------

`toolz` supports Python 2.6+ and Python 3.2+ with a common codebase.  It is
pure Python and requires no dependencies beyond the standard library.
