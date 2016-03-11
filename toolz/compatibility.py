from functools import reduce
import inspect
import operator
import sys
PY3 = sys.version_info[0] > 2

__all__ = ('PY3', 'map', 'filter', 'range', 'zip', 'reduce', 'zip_longest',
           'iteritems', 'iterkeys', 'itervalues', 'filterfalse')

# This is a kludge for Python 3.4.0 support
# currently len(inspect.getargspec(map).args) == 0, a wrong result.
# As this is fixed in future versions then hopefully this kludge can be
# removed.
known_numargs = {map: 2, filter: 2, reduce: 2}


def _num_required_args_p2(func):
    """ Number of args for func

    >>> def foo(a, b, c=None):
    ...     return a + b + c

    >>> _num_required_args(foo)
    2

    >>> def bar(*args):
    ...     return sum(args)

    >>> print(_num_required_args(bar))
    None
    """
    if func in known_numargs:
        return known_numargs[func]
    try:
        spec = inspect.getfullargspec(func)
        if spec.varargs:
            return None
        num_defaults = len(spec.defaults) if spec.defaults else 0
        return len(spec.args) - num_defaults           
    except TypeError:
        return None

def _num_required_args_p3(func):
    """ See description of _num_required_args_p3
    """
    if func in known_numargs:
        return known_numargs[func]
    try:
        required_args = 0
        for param in inspect.signature(func).parameters.values():
            kind = param.kind
            # Presence of *args or **kwargs precludes a requirement.
            if kind in [param.VAR_POSITIONAL, param.VAR_KEYWORD]:
                return None
            # Keyword only arguments, and ones with a default aren't required.
            elif kind == param.KEYWORD_ONLY or param.default != inspect._empty:
                continue
            elif kind in [param.POSITIONAL_OR_KEYWORD, param.POSITIONAL_ONLY]:
                required_args += 1
            else:
                raise AttributeError("Invalid kind found")
        return required_args
    except TypeError:
        return None


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
    num_required_args = _num_required_args_p3
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
    num_required_args = _num_required_args_p2
