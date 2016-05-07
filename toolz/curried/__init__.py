"""
Alternate namespace for toolz such that all functions are curried

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
from . import exceptions
from . import operator
import toolz


def _should_curry(func):
    if not callable(func) or isinstance(func, toolz.curry):
        return False
    nargs = toolz.functoolz.num_required_args(func)
    if nargs is None or nargs > 1:
        return True
    return nargs == 1 and toolz.functoolz.has_keywords(func)


def _curry_namespace(ns):
    return dict(
        (name, toolz.curry(f) if _should_curry(f) else f)
        for name, f in ns.items() if '__' not in name
    )


locals().update(toolz.merge(
    _curry_namespace(vars(toolz)),
    _curry_namespace(vars(exceptions)),
))

# Clean up the namespace.
del _should_curry
del exceptions
del toolz
