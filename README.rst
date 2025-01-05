Toolz
=====

|Build Status| |Coverage Status| |Version Status|

A set of utility functions for iterators, functions, and dictionaries.

See the PyToolz documentation at https://toolz.readthedocs.io

LICENSE
-------

New BSD. See `License File <https://github.com/pytoolz/toolz/blob/master/LICENSE.txt>`__.

Install
-------

``toolz`` is on the Python Package Index (PyPI):

::

    pip install toolz

Structure and Heritage
----------------------

``toolz`` is implemented in three parts:

|literal itertoolz|_, for operations on iterables. Examples: ``groupby``,
``unique``, ``interpose``,

|literal functoolz|_, for higher-order functions. Examples: ``memoize``,
``curry``, ``compose``,

|literal dicttoolz|_, for operations on dictionaries. Examples: ``assoc``,
``update-in``, ``merge``.

.. |literal itertoolz| replace:: ``itertoolz``
.. _literal itertoolz: https://github.com/pytoolz/toolz/blob/master/toolz/itertoolz.py

.. |literal functoolz| replace:: ``functoolz``
.. _literal functoolz: https://github.com/pytoolz/toolz/blob/master/toolz/functoolz.py

.. |literal dicttoolz| replace:: ``dicttoolz``
.. _literal dicttoolz: https://github.com/pytoolz/toolz/blob/master/toolz/dicttoolz.py

These functions come from the legacy of functional languages for list
processing. They interoperate well to accomplish common complex tasks.

Read our `API
Documentation <https://toolz.readthedocs.io/en/latest/api.html>`__ for
more details.

Example
-------

This builds a standard wordcount function from pieces within ``toolz``:

.. code:: python

    >>> def stem(word):
    ...     """ Stem word to primitive form """
    ...     return word.lower().rstrip(",.!:;'-\"").lstrip("'\"")

    >>> from toolz import compose, frequencies
    >>> from toolz.curried import map
    >>> wordcount = compose(frequencies, map(stem), str.split)

    >>> sentence = "This cat jumped over this other cat!"
    >>> wordcount(sentence)
    {'this': 2, 'cat': 2, 'jumped': 1, 'over': 1, 'other': 1}

Dependencies
------------

``toolz`` supports Python 3.8+ with a common codebase.
It is pure Python and requires no dependencies beyond the standard
library.

It is, in short, a lightweight dependency.


CyToolz
-------

The ``toolz`` project has been reimplemented in `Cython <http://cython.org>`__.
The ``cytoolz`` project is a drop-in replacement for the Pure Python
implementation.
See `CyToolz GitHub Page <https://github.com/pytoolz/cytoolz/>`__ for more
details.

See Also
--------

-  `Underscore.js <https://underscorejs.org/>`__: A similar library for
   JavaScript
-  `Enumerable <https://ruby-doc.org/core-2.0.0/Enumerable.html>`__: A
   similar library for Ruby
-  `Clojure <https://clojure.org/>`__: A functional language whose
   standard library has several counterparts in ``toolz``
-  `itertools <https://docs.python.org/2/library/itertools.html>`__: The
   Python standard library for iterator tools
-  `functools <https://docs.python.org/2/library/functools.html>`__: The
   Python standard library for function tools

Project Status
--------------

**This project is alive but inactive.**

The original maintainers have mostly moved on to other endeavors.  We're still
around for critical bug fixes, Python version bumps, and security issues and
will commit to keeping the project alive (it's highly depended upon).
However, beyond that we don't plan to spend much time reviewing contributions.
We view Toolz as mostly complete.

We encourage enthusiasts to innovate in new and wonderful places 🚀

.. |Build Status| image:: https://github.com/pytoolz/toolz/actions/workflows/test.yml/badge.svg?branch=master
   :target: https://github.com/pytoolz/toolz/actions
.. |Coverage Status| image:: https://codecov.io/gh/pytoolz/toolz/graph/badge.svg?token=4ZFc9dwKqY
   :target: https://codecov.io/gh/pytoolz/toolz
.. |Version Status| image:: https://badge.fury.io/py/toolz.svg
   :target: https://badge.fury.io/py/toolz
