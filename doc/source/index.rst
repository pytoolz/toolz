
PyToolz API Documentation
=========================

Toolz provides a set of utility functions for iterators, functions,
and dictionaries.  These functions interoperate well and form
the building blocks of common data analytic operations.  They extend the
standard libraries `itertools` and `functools` and borrow heavily from the
standard libraries of contemporary functional languages.

Toolz provides a suite of functions which have the following functional virtues:

-   **Composable:** They interoperate due to their use of core data structures.
-   **Pure:**  They don't change their inputs or rely on external state.
-   **Lazy:**  They don't run until absolutely necessary, allowing them to support large streaming data sets.

Toolz functions are *pragmatic*.  They understand that most programmers
have deadlines.

-   **Low Tech:** They're just functions, no syntax or magic tricks to learn
-   **Tuned:** They're profiled and optimized
-   **Serializable:** They support common solutions for parallel computing

This gives developers the power to write *powerful* programs to solve *complex
problems* with relatively *simple code*.  This code can be *easy to understand*
without sacrificing *performance*.  Toolz enables this approach, commonly
associated with functional programming, within a natural Pythonic style
suitable for most developers.

BSD licensed source code is available at http://github.com/pytoolz/toolz/ .


Contents
^^^^^^^^

.. toctree::
   :maxdepth: 2

   heritage.rst
   install.rst
   composition.rst
   purity.rst
   laziness.rst
   control.rst
   curry.rst
   streaming-analytics.rst
   parallelism.rst
   api.rst
   tips-and-tricks.rst
   references.rst
