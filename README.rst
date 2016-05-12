Toolz
=====

|Build Status| |Coverage Status| |Version Status| |Downloads|

A set of utility functions for iterators, functions, and dictionaries.

See the PyToolz documentation at http://toolz.readthedocs.org

LICENSE
-------

New BSD. See `License File <https://github.com/pytoolz/toolz/blob/master/LICENSE.txt>`__.

Install
-------

``toolz`` is on the Python Package Index (PyPI):

::

    pip install toolz

or

::

    easy_install toolz

Structure and Heritage
----------------------

``toolz`` is implemented in three parts:

|literal itertoolz|_, for operations on iterables. Examples: ``groupby``,
``unique``, ``interpose``,

|literal functoolz|_, for higher-order functions. Examples: ``memoize``,
``curry``, ``compose``

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
Documentation <http://toolz.readthedocs.org/en/latest/api.html>`__ for
more details.

Example
-------

This builds a standard wordcount function from pieces within ``toolz``:

.. code:: python

    >>> def stem(word):
    ...     """ Stem word to primitive form """
    ...     return word.lower().rstrip(",.!:;'-\"").lstrip("'\"")

    >>> from toolz import compose, frequencies, partial
    >>> from toolz.curried import map
    >>> wordcount = compose(frequencies, map(stem), str.split)

    >>> sentence = "This cat jumped over this other cat!"
    >>> wordcount(sentence)
    {'this': 2, 'cat': 2, 'jumped': 1, 'over': 1, 'other': 1}

Dependencies
------------

``toolz`` supports Python 2.6+ and Python 3.3+ with a common codebase.
It is pure Python and requires no dependencies beyond the standard
library.

It is, in short, a light weight dependency.


CyToolz
-------

The ``toolz`` project has been reimplemented in `Cython <http://cython.org>`__.
The ``cytoolz`` project is a drop-in replacement for the Pure Python
implementation.
See `CyToolz Github Page <https://github.com/pytoolz/cytoolz/>`__ for more
details.

See Also
--------

-  `Underscore.js <http://underscorejs.org>`__: A similar library for
   JavaScript
-  `Enumerable <http://ruby-doc.org/core-2.0.0/Enumerable.html>`__: A
   similar library for Ruby
-  `Clojure <http://clojure.org>`__: A functional language whose
   standard library has several counterparts in ``toolz``
-  `itertools <http://docs.python.org/2/library/itertools.html>`__: The
   Python standard library for iterator tools
-  `functools <http://docs.python.org/2/library/functools.html>`__: The
   Python standard library for function tools

Contributions Welcome
---------------------

``toolz`` aims to be a repository for utility functions, particularly
those that come from the functional programming and list processing
traditions. We welcome contributions that fall within this scope.

We also try to keep the API small to keep ``toolz`` manageable.  The ideal
contribution is significantly different from existing functions and has
precedent in a few other functional systems.

Please take a look at our
`issue page <https://github.com/pytoolz/toolz/issues>`__
for contribution ideas.

Community
---------

See our `mailing list <https://groups.google.com/forum/#!forum/pytoolz>`__.
We're friendly.

.. |Build Status| image:: https://travis-ci.org/pytoolz/toolz.svg?branch=master
   :target: https://travis-ci.org/pytoolz/toolz
.. |Coverage Status| image:: https://coveralls.io/repos/pytoolz/toolz/badge.svg?branch=master
   :target: https://coveralls.io/r/pytoolz/toolz
.. |Version Status| image:: https://badge.fury.io/py/toolz.svg
   :target: http://badge.fury.io/py/toolz
.. |Downloads| image:: https://img.shields.io/pypi/dm/toolz.svg
   :target: https://pypi.python.org/pypi/toolz/
