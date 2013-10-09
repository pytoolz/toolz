.. Toolz documentation master file, created by
   sphinx-quickstart on Sun Sep 22 18:06:00 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Toolz API Documentation
=======================

The Toolz project provides a set of utility functions for iterators, functions,
and dictionaries.  These functions are designed to interoperate well, forming
the building blocks of common data analytic operations.  They extend the
standard libraries `itertools` and `functools`.

Toolz provides a suite of functions which have the following virtues:

-   **Composable**: They interoperate due to their use of core data structures
-   **Pure**:  They don't change their inputs or rely on external state
-   **Lazy**:  They don't run until absolutely necessary, allowing them to
           support large streaming data sets

This gives developers the power to write *powerful* programs to solve *complex
problems* with relatively *simple code* which is *easy to understand* without
sacrificing *performance*.  Toolz enables this approach, commonly associated
with functional programming, within a natural Pythonic style suitable for
most developers.

Contents
^^^^^^^^

.. toctree::
   :maxdepth: 2

   heritage.rst
   api.rst
   install.rst
   references.rst

Back Matter
^^^^^^^^^^^

* :ref:`genindex`
* :ref:`search`

