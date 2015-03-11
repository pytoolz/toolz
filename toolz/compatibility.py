import operator
import sys

from functools import partial, WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES

PY3 = sys.version_info[0] > 2

__all__ = ('PY3', 'map', 'filter', 'range', 'zip', 'reduce', 'zip_longest',
           'iteritems', 'iterkeys', 'itervalues', 'filterfalse')

if PY3:
    map = map
    filter = filter
    range = range
    zip = zip
    from functools import reduce
    from itertools import zip_longest
    from itertools import filterfalse
    iteritems = operator.methodcaller('items')
    iterkeys = operator.methodcaller('keys')
    itervalues = operator.methodcaller('values')
else:
    range = xrange
    reduce = reduce
    from itertools import imap as map
    from itertools import ifilter as filter
    from itertools import ifilterfalse as filterfalse
    from itertools import izip as zip
    from itertools import izip_longest as zip_longest
    iteritems = operator.methodcaller('iteritems')
    iterkeys = operator.methodcaller('iterkeys')
    itervalues = operator.methodcaller('itervalues')


# backport of Python 3.4 update_wrapper which has
# much smarter behavior than other versions
def update_wrapper(wrapper,
                   wrapped,
                   assigned=WRAPPER_ASSIGNMENTS,
                   updated=WRAPPER_UPDATES):

    """Makes wrapper appear as the wrapped callable.

    Backport of Python3.4's functools.update_wrapper. This version is
    more intelligent than what's found in Python 2 as it uses a
    try/except/else block when moving attributes rather than just
    charitably assuming the attributes are present.

    It also backports Python 3's `__wrapped__` attribute as well
    to give access to the original callable.

    WARNING: This function modifies the wrapper function.

    More useful for class based decorator than closure based decorators.

    >>> class Decorator(object):
    ...     def __init__(self, f):
    ...         update_wrapper(self, f)
    ...         self._f = f
    ...     def __call__(self, *a, **k):
    ...         return self._f(*a, **k)

    >>> @Decorator
    ... def add(a, b):
    ...     "a doc string"
    ...     return a + b

    >>> print(add.__name__)
    add
    >>> print(add.__doc__)
    a doc string
    """

    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)

    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))

    # store original callable last so it's not accidentally copied over
    wrapper.__wrapped__ = wrapped

    # return wrapper for use as a decorator
    return wrapper


def wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES):
    """Decorator form of updated version of update_wrapper.

    This is very useful for writing closure based decorators
    rather than using update_wrapper manually on the closure.

    WARNING: This function modifies what it's applied to.

    >>> def decorator(f):
    ...     @wraps(f)
    ...     def wrapper(*a, **k):
    ...         return f(*a, **k)
    ...     return wrapper

    >>> @decorator
    ... def add(a, b):
    ...     "a doc string"
    ...     return a+b

    >>> print(add.__name__)
    add

    >>> print(add.__doc__)
    a doc string
    """
    # return partial to use as a decorator
    return partial(update_wrapper, wrapped=wrapped,  # noqa
           assigned=assigned, updated=updated)  # noqa
