Toolz
=====

A set of utility functions for iterators, functions, and dictionaries.

[![Build Status](https://travis-ci.org/pytoolz/toolz.png)](https://travis-ci.org/pytoolz/toolz)


LICENSE
-------

New BSD.  See [License File](LICENSE.TXT).

Install
-------

`toolz` is on the Python Package Index (PyPi):

    pip install toolz

or

    easy_install toolz

Structure and Heritage
----------------------

`toolz` is implemented in three parts:

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

This builds a standard wordcount function from pieces within `toolz`:

    >>> def stem(word):
    ...     """ Stem word to primitive form """
    ...     return word.lower().rstrip(",.!:;'-\"").lstrip("'\"")

    >>> from toolz import comp, frequencies
    >>> from functools import partial
    >>> wordcount = comp(frequencies, partial(map, stem), str.split)

    >>> sentence = "This cat jumped over this other cat!"
    >>> wordcount(sentence)
    {'this': 2, 'cat': 2, 'jumped': 1, 'over': 1, 'other': 1}


Dependencies
------------

`toolz` supports Python 2.6+ and Python 3.2+ with a common codebase.  It is
pure Python and requires no dependencies beyond the standard library.


See Also
--------

*   [Underscore.js](http://underscorejs.org): A similar library for JavaScript
*   [Enumerable](http://ruby-doc.org/core-2.0.0/Enumerable.html): A similar
    library for Ruby
*   [Clojure](http://clojure.org): A functional language whose standard library
    has several counterparts in `toolz`
*   [itertools](http://docs.python.org/2/library/itertools.html): The
    Python standard library for iterator tools
*   [functools](http://docs.python.org/2/library/functools.html): The
    Python standard library for function tools


Contributions Welcome
---------------------

`toolz` aims to be a repository for utility functions, particularly those that
come from the functional programming and list processing traditions.
We welcome contributions that fall within this scope and encourage users to
scrape their `util.py` files for functions that are broadly useful.

Please take a look at our [issue page](https://github.com/pytoolz/toolz/issues)
for contribution ideas.
