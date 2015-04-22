from functools import reduce, partial
import inspect
import operator
import sys


__all__ = ('identity', 'thread_first', 'thread_last', 'memoize', 'compose',
           'pipe', 'complement', 'juxt', 'do', 'curry')


def identity(x):
    """ Identity function. Return x

    >>> identity(3)
    3
    """
    return x


def thread_first(val, *forms):
    """ Thread value through a sequence of functions/forms

    >>> def double(x): return 2*x
    >>> def inc(x):    return x + 1
    >>> thread_first(1, inc, double)
    4

    If the function expects more than one input you can specify those inputs
    in a tuple.  The value is used as the first input.

    >>> def add(x, y): return x + y
    >>> def pow(x, y): return x**y
    >>> thread_first(1, (add, 4), (pow, 2))  # pow(add(1, 4), 2)
    25

    So in general
        thread_first(x, f, (g, y, z))
    expands to
        g(f(x), y, z)

    See Also:
        thread_last
    """
    def evalform_front(val, form):
        if callable(form):
            return form(val)
        if isinstance(form, tuple):
            func, args = form[0], form[1:]
            args = (val,) + args
            return func(*args)
    return reduce(evalform_front, forms, val)


def thread_last(val, *forms):
    """ Thread value through a sequence of functions/forms

    >>> def double(x): return 2*x
    >>> def inc(x):    return x + 1
    >>> thread_last(1, inc, double)
    4

    If the function expects more than one input you can specify those inputs
    in a tuple.  The value is used as the last input.

    >>> def add(x, y): return x + y
    >>> def pow(x, y): return x**y
    >>> thread_last(1, (add, 4), (pow, 2))  # pow(2, add(4, 1))
    32

    So in general
        thread_last(x, f, (g, y, z))
    expands to
        g(y, z, f(x))

    >>> def iseven(x):
    ...     return x % 2 == 0
    >>> list(thread_last([1, 2, 3], (map, inc), (filter, iseven)))
    [2, 4]

    See Also:
        thread_first
    """
    def evalform_back(val, form):
        if callable(form):
            return form(val)
        if isinstance(form, tuple):
            func, args = form[0], form[1:]
            args = args + (val,)
            return func(*args)
    return reduce(evalform_back, forms, val)


# This is a kludge for Python 3.4.0 support
# currently len(inspect.getargspec(map).args) == 0, a wrong result.
# As this is fixed in future versions then hopefully this kludge can be
# removed.
known_numargs = {map: 2, filter: 2, reduce: 2}


def _num_required_args(func):
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
        spec = inspect.getargspec(func)
        if spec.varargs:
            return None
        num_defaults = len(spec.defaults) if spec.defaults else 0
        return len(spec.args) - num_defaults
    except TypeError:
        return None


class curry(object):
    """ Curry a callable function

    Enables partial application of arguments through calling a function with an
    incomplete set of arguments.

    >>> def mul(x, y):
    ...     return x * y
    >>> mul = curry(mul)

    >>> double = mul(2)
    >>> double(10)
    20

    Also supports keyword arguments

    >>> @curry                  # Can use curry as a decorator
    ... def f(x, y, a=10):
    ...     return a * (x + y)

    >>> add = f(a=1)
    >>> add(2, 3)
    5

    See Also:
        toolz.curried - namespace of curried functions
                        http://toolz.readthedocs.org/en/latest/curry.html
    """
    def __init__(self, *args, **kwargs):
        if not args:
            raise TypeError('__init__() takes at least 2 arguments (1 given)')
        func, args = args[0], args[1:]
        if not callable(func):
            raise TypeError("Input must be callable")

        # curry- or functools.partial-like object?  Unpack and merge arguments
        if (hasattr(func, 'func')
                and hasattr(func, 'args')
                and hasattr(func, 'keywords')
                and isinstance(func.args, tuple)):
            _kwargs = {}
            if func.keywords:
                _kwargs.update(func.keywords)
            _kwargs.update(kwargs)
            kwargs = _kwargs
            args = func.args + args
            func = func.func

        if kwargs:
            self._partial = partial(func, *args, **kwargs)
        else:
            self._partial = partial(func, *args)

        self.__doc__ = getattr(func, '__doc__', None)
        self.__name__ = getattr(func, '__name__', '<curry>')

    @property
    def func(self):
        return self._partial.func

    @property
    def args(self):
        return self._partial.args

    @property
    def keywords(self):
        return self._partial.keywords

    @property
    def func_name(self):
        return self.__name__

    def __str__(self):
        return str(self.func)

    def __repr__(self):
        return repr(self.func)

    def __hash__(self):
        return hash((self.func, self.args,
                     frozenset(self.keywords.items()) if self.keywords
                     else None))

    def __eq__(self, other):
        return (isinstance(other, curry) and self.func == other.func and
                self.args == other.args and self.keywords == other.keywords)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __call__(self, *args, **kwargs):
        try:
            return self._partial(*args, **kwargs)
        except TypeError:
            # If there was a genuine TypeError
            required_args = _num_required_args(self.func)
            if (required_args is not None and
                    len(args) + len(self.args) >= required_args):
                raise

        return curry(self._partial, *args, **kwargs)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return curry(self, instance)

    # pickle protocol because functools.partial objects can't be pickled
    def __getstate__(self):
        # dictoolz.keyfilter, I miss you!
        userdict = tuple((k, v) for k, v in self.__dict__.items()
                         if k != '_partial')
        return self.func, self.args, self.keywords, userdict

    def __setstate__(self, state):
        func, args, kwargs, userdict = state
        self.__init__(func, *args, **(kwargs or {}))
        self.__dict__.update(userdict)


def has_kwargs(f):
    """ Does a function have keyword arguments?

    >>> def f(x, y=0):
    ...     return x + y

    >>> has_kwargs(f)
    True
    """
    if sys.version_info[0] == 2:  # pragma: no cover
        spec = inspect.getargspec(f)
        return bool(spec and (spec.keywords or spec.defaults))
    if sys.version_info[0] == 3:  # pragma: no cover
        spec = inspect.getfullargspec(f)
        return bool(spec.defaults)


def isunary(f):
    """ Does a function have only a single argument?

    >>> def f(x):
    ...     return x

    >>> isunary(f)
    True
    >>> isunary(lambda x, y: x + y)
    False
    """
    try:
        if sys.version_info[0] == 2:  # pragma: no cover
            spec = inspect.getargspec(f)
        if sys.version_info[0] == 3:  # pragma: no cover
            spec = inspect.getfullargspec(f)
        return bool(spec and spec.varargs is None and not has_kwargs(f)
                    and len(spec.args) == 1)
    except TypeError:  # pragma: no cover
        return None    # in Python < 3.4 builtins fail, return None


@curry
def memoize(func, cache=None, key=None):
    """ Cache a function's result for speedy future evaluation

    Considerations:
        Trades memory for speed.
        Only use on pure functions.

    >>> def add(x, y):  return x + y
    >>> add = memoize(add)

    Or use as a decorator

    >>> @memoize
    ... def add(x, y):
    ...     return x + y

    Use the ``cache`` keyword to provide a dict-like object as an initial cache

    >>> @memoize(cache={(1, 2): 3})
    ... def add(x, y):
    ...     return x + y

    Note that the above works as a decorator because ``memoize`` is curried.

    It is also possible to provide a ``key(args, kwargs)`` function that
    calculates keys used for the cache, which receives an ``args`` tuple and
    ``kwargs`` dict as input, and must return a hashable value.  However,
    the default key function should be sufficient most of the time.

    >>> # Use key function that ignores extraneous keyword arguments
    >>> @memoize(key=lambda args, kwargs: args)
    ... def add(x, y, verbose=False):
    ...     if verbose:
    ...         print('Calculating %s + %s' % (x, y))
    ...     return x + y
    """
    if cache is None:
        cache = {}

    try:
        may_have_kwargs = has_kwargs(func)
        # Is unary function (single arg, no variadic argument or keywords)?
        is_unary = isunary(func)
    except TypeError:  # pragma: no cover
        may_have_kwargs = True
        is_unary = False

    def memof(*args, **kwargs):
        try:
            if key is not None:
                k = key(args, kwargs)
            elif is_unary:
                k = args[0]
            elif may_have_kwargs:
                k = (args or None,
                     frozenset(kwargs.items()) if kwargs else None)
            else:
                k = args

            in_cache = k in cache
        except TypeError:
            raise TypeError("Arguments to memoized function must be hashable")

        if in_cache:
            return cache[k]
        else:
            result = func(*args, **kwargs)
            cache[k] = result
            return result

    try:
        memof.__name__ = func.__name__
    except AttributeError:
        pass
    memof.__doc__ = func.__doc__
    return memof


class Compose(object):
    """ A composition of functions

    See Also:
        compose
    """
    __slots__ = ['funcs']

    def __init__(self, *funcs):
        self.funcs = funcs

    def __call__(self, *args, **kwargs):
        fns = list(reversed(self.funcs))
        ret = fns[0](*args, **kwargs)
        for f in fns[1:]:
            ret = f(ret)
        return ret

    def __getstate__(self):
        return self.funcs

    def __setstate__(self, state):
        self.funcs = tuple(state)


def compose(*funcs):
    """ Compose functions to operate in series.

    Returns a function that applies other functions in sequence.

    Functions are applied from right to left so that
    ``compose(f, g, h)(x, y)`` is the same as ``f(g(h(x, y)))``.

    If no arguments are provided, the identity function (f(x) = x) is returned.

    >>> inc = lambda i: i + 1
    >>> compose(str, inc)(3)
    '4'

    See Also:
        pipe
    """
    if not funcs:
        return identity
    if len(funcs) == 1:
        return funcs[0]
    else:
        return Compose(*funcs)


def pipe(data, *funcs):
    """ Pipe a value through a sequence of functions

    I.e. ``pipe(data, f, g, h)`` is equivalent to ``h(g(f(data)))``

    We think of the value as progressing through a pipe of several
    transformations, much like pipes in UNIX

    ``$ cat data | f | g | h``

    >>> double = lambda i: 2 * i
    >>> pipe(3, double, str)
    '6'

    See Also:
        compose
        thread_first
        thread_last
    """
    for func in funcs:
        data = func(data)
    return data


def complement(func):
    """ Convert a predicate function to its logical complement.

    In other words, return a function that, for inputs that normally
    yield True, yields False, and vice-versa.

    >>> def iseven(n): return n % 2 == 0
    >>> isodd = complement(iseven)
    >>> iseven(2)
    True
    >>> isodd(2)
    False
    """
    return compose(operator.not_, func)


class juxt(object):
    """
    Creates a function that calls several functions with the same arguments.

    Takes several functions and returns a function that applies its arguments
    to each of those functions then returns a tuple of the results.

    Name comes from juxtaposition: the fact of two things being seen or placed
    close together with contrasting effect.

    >>> inc = lambda x: x + 1
    >>> double = lambda x: x * 2
    >>> juxt(inc, double)(10)
    (11, 20)
    >>> juxt([inc, double])(10)
    (11, 20)
    """
    __slots__ = ['funcs']

    def __init__(self, *funcs):
        if len(funcs) == 1 and not callable(funcs[0]):
            funcs = funcs[0]
        self.funcs = tuple(funcs)

    def __call__(self, *args, **kwargs):
        return tuple(func(*args, **kwargs) for func in self.funcs)

    def __getstate__(self):
        return self.funcs

    def __setstate__(self, state):
        self.funcs = state


def do(func, x):
    """ Runs ``func`` on ``x``, returns ``x``

    Because the results of ``func`` are not returned, only the side
    effects of ``func`` are relevant.

    Logging functions can be made by composing ``do`` with a storage function
    like ``list.append`` or ``file.write``

    >>> from toolz import compose
    >>> from toolz.curried import do

    >>> log = []
    >>> inc = lambda x: x + 1
    >>> inc = compose(inc, do(log.append))
    >>> inc(1)
    2
    >>> inc(11)
    12
    >>> log
    [1, 11]

    """
    func(x)
    return x
