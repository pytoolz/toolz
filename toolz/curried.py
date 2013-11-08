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
    >>> data = [(1, 2), (11, 22), (111, 222)])
    >>> map(lambda seq: get(0, seq), data)
    [1, 11, 111]

    The curried version allows simple expression of partial evaluation
    >>> map(get(0), data)
    [1, 11, 111]

See Also:
    toolz.functoolz.curry
"""

import toolz
from .functoolz import curry
import inspect


def nargs(f):
    try:
        return len(inspect.getargspec(f).args)
    except TypeError:
        return None


def should_curry(f):
    do_curry = set((toolz.map, toolz.filter, toolz.sorted))
    return (callable(f) and nargs(f) and nargs(f) > 1
            or f in do_curry)


d = dict((name, curry(f) if '__' not in name and should_curry(f) else f)
         for name, f in toolz.__dict__.items())


locals().update(d)


@curry
def merge_with(func, *dicts):
    if len(dicts) == 0:
        raise TypeError("No input")
    return toolz.merge_with(func, *dicts)


merge_with.__doc__ = toolz.merge_with.__doc__
