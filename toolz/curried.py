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

import toolz
import inspect

_numargs = {
    # built-ins
    toolz.filter: 2,
    toolz.map: 2,
    toolz.reduce: 2,
    toolz.sorted: 1,

    # exceptions
    toolz.merge_sorted: 1,
    toolz.merge_with: 2,
}


def _should_curry(f):
    if f in _numargs:
        return True
    if isinstance(f, toolz.functoolz.Curry):
        return False
    try:
        spec = inspect.getargspec(f)
        has_kwargs = bool(spec.defaults) or bool(spec.keywords)
        numargs = len(spec.args) - len(spec.defaults or ())
        if has_kwargs:
            return numargs > 0
        else:
            return numargs > 1
    except TypeError:
        return False


_d = dict(
    (name, toolz.curry(f, numargs=_numargs.get(f)) if _should_curry(f) else f)
    for name, f in toolz.__dict__.items()
    if '__' not in name)

locals().update(_d)
