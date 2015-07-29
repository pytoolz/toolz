import inspect

import toolz


def _nargs(f):
    try:
        return len(inspect.getargspec(f).args)
    except TypeError:
        return 0


def should_curry(f):
    do_curry = frozenset((toolz.map, toolz.filter, toolz.sorted, toolz.reduce))
    return callable(f) and (_nargs(f) > 1 or f in do_curry)
