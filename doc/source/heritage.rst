Heritage
========

While Python was originally intended as an imperative language
[Guido_], it contains all elements necessary to support a rich set of features
from the functional paradigm.  In particular its core data structures, lazy
iterators, and functions as first class objects can be combined to implement a
common standard library of functions shared among many functional languages.

This was first recognized and supported through the standard libraries
itertools_ and functools_ which contain functions like ``permutations``,
``chain`` and ``partial`` to complement the standard ``map``, ``filter``,
``reduce`` already found in the core language.  While these libraries contain
substantial functionality they do not achieve the same level of adoption found
in similar projects in other languages.  This may be because they are
incomplete and lack a number of commonly related functions like ``compose`` and
``groupby`` which often complement these core operations.

A completion of this set of functions was first attempted in the projects
itertoolz_ and functoolz_ (note the z).  These libraries contained
several functions that were absent in the standard itertools_/functools_
libraries.  The ``itertoolz``/``functoolz`` libraries were eventually merged
into the monolithic ``toolz`` project described here.

Most contemporary functional languages (Haskell, Scala, Clojure, ...) contain
some variation of the functions found in ``toolz``.  The ``toolz`` project
generally adheres closely to the API found in the Clojure standard library (see
cheatsheet_) and where disagreements occur that API usually dominates.  The
``toolz`` API is also strongly affected by the principles of the Python
language itself, and often makes deviations in order to be more approachable to
that community.

The development of a functional standard library within a popular imperative
language is not unique.  Similar projects have arisen in other
imperative-by-design languages that contain the necessary elements to support a
functional standard library.  Underscore.js_ in JavaScript has attained
notable popularity in the web community.  ``LINQ`` in C# follows a similar
philosophy but mimics declarative database languages rather than functional
ones.  Enumerable_ is is the closest project in Ruby.  Other excellent projects
also exist within the Python ecosystem, most notably Fn.py_ and Funcy_.

.. [itertools] https://docs.python.org/2/library/itertools.html
.. [functools] https://docs.python.org/2/library/functools.html
.. [itertoolz] https://github.com/mrocklin/itertoolz
.. [functoolz] https://github.com/mrocklin/functoolz
.. [Underscore.js] https://underscorejs.org
.. [cheatsheet] https://clojure.org/cheatsheet
.. [Guido] https://python-history.blogspot.com/2009/04/origins-of-pythons-functional-features.html
.. [Enumerable] https://ruby-doc.org/core-2.0.0/Enumerable.html
.. [funcy] https://github.com/suor/funcy/
.. [fn.py] https://github.com/kachayev/fn.py
