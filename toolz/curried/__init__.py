"""
Alternate namespece for toolz such that all functions are curried

Currying provides implicit partial evaluation of all functions

Example:

    Get usually requires two arguments, an index and a collection
    >>> from toolz.curried import get
    >>> get(0, ('a', 'b'))
    'a'

    When we use it in higher order functions we often want to pass a partially
    evaluated form
    >>> data = [(1, 2), (11, 22), (111, 222)]
    >>> list(map(lambda seq: get(0, seq), data))
    [1, 11, 111]

    The curried version allows simple expression of partial evaluation
    >>> list(map(get(0), data))
    [1, 11, 111]

See Also:
    toolz.functoolz.curry
"""
from .core import should_curry
from .operator import *

import toolz


locals().update(
    dict((name, toolz.curry(f) if should_curry(f) else f)
         for name, f in vars(toolz).items() if '__' not in name),
)

# Clean up the namespace.
del toolz
del should_curry


# This should come after the previous `locals().update` call to make
# sure the exceptions get added to the namespace.
from .exceptions import *
