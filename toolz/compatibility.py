import operator
import sys
PY3 = sys.version_info[0] > 2
PY33 = sys.version_info[0] == 3 and sys.version_info[1] == 3
PY34 = sys.version_info[0] == 3 and sys.version_info[1] >= 4
PYPY = hasattr(sys, 'pypy_version_info')

__all__ = ('map', 'filter', 'range', 'zip', 'reduce', 'zip_longest',
           'iteritems', 'iterkeys', 'itervalues', 'filterfalse',
           'PY3', 'PY34', 'PYPY', 'import_module', 'singledispatch')

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

if PY34:
    from functools import singledispatch
else:
    from functools import partial, update_wrapper

    def singledispatch(f):
        """ Simple singledispatch implementation
        >>> class C:
        ...     def __init__(self, x):
        ...         self.x = x
        >>> a = C(1)
        >>> b = {'x': 2}
        >>> @singledispatch
        ... def get(o, key):
        ...     return getattr(o, key)
        >>> @get.register(dict)
        ... def _(d, key):
        ...     return d[key]
        >>> get(a, 'x')
        1
        >>> get(b, 'x')
        2
        """
        registry = {}

        def register(cls, func=None):
            if not func:
                return partial(register, cls)

            registry[cls] = func

        def dispatch(cls):
            return registry.get(cls, f)

        def wrapper(*args, **kwargs):
            return dispatch(type(args[0]))(*args, **kwargs)

        wrapper.registry = registry
        wrapper.dispatch = dispatch
        wrapper.register = register
        update_wrapper(wrapper, f)

        return wrapper


try:
    from importlib import import_module
except ImportError:
    def import_module(name):
        __import__(name)
        return sys.modules[name]
