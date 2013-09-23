Toolz
=====

This library provides a set of utility functions for Python, mostly to
implement common functional idioms, emphasizing immutability and
composability. It includes various higher-order functions, as well as
functions for operating on sequences and maps (dictionaries).

[![Build Status](https://travis-ci.org/pytoolz/toolz.png)](https://travis-ci.org/pytoolz/toolz)

Toolz is implemented in three parts:

* [`itertoolz`](https://github.com/pytoolz/toolz/blob/master/toolz/itertoolz/core.py), for opertions on iterables (sequences).  Examples: `groupby`, `concat`, `interpose`, `interleave`.
* [`functoolz`](https://github.com/pytoolz/toolz/blob/master/toolz/functoolz/core.py), for higher-order functions.  Examples: `comp`, `memoize`, `iterate`.
* [`dicttoolz`](https://github.com/pytoolz/toolz/blob/master/toolz/dicttoolz/core.py), for operations on dictionaries.  Examples: `assoc`, `update-in`, `merge`.

These three are implemented as separate directories but are imported from a single module.  For example,

    >>> from toolz import groupby, comp
    >>> square = lambda x: x * x
    >>> small = lambda x: x < 10
    >>> groupby(comp(small, square), range(10))
    {False: [4, 5, 6, 7, 8, 9], True: [0, 1, 2, 3]}

Author
------

[Matthew Rocklin](http://matthewrocklin.com)

LICENSE
-------

New BSD.  See [License File](LICENSE.TXT).

Install
-------

`toolz` is on the Python Package Index (PyPi)

    pip install toolz

or 
    
    easy_install toolz

Dependencies
------------

`toolz` supports Python 2.6+ and Python 3.2+ with a common codebase.
