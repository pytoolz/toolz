from functools import reduce, partial
import inspect
import operator


__all__ = ('identity', 'thread_first', 'thread_last', 'memoize', 'compose',
           'pipe', 'complement', 'juxt', 'do', 'curry')


def identity(x):
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
    def __init__(self, func, *args, **kwargs):
        if not callable(func):
            raise TypeError("Input must be callable")

        self.func = func
        self.args = args
        self.keywords = kwargs if kwargs else None
        self.__doc__ = self.func.__doc__
        try:
            self.func_name = self.func.func_name
        except AttributeError:
            pass

    def __str__(self):
        return str(self.func)

    def __repr__(self):
        return repr(self.func)

    def __call__(self, *args, **_kwargs):
        args = self.args + args
        if _kwargs:
            kwargs = {}
            if self.keywords:
                kwargs.update(self.keywords)
            kwargs.update(_kwargs)
        elif self.keywords:
            kwargs = self.keywords
        else:
            kwargs = {}

        try:
            return self.func(*args, **kwargs)
        except TypeError:
            required_args = _num_required_args(self.func)

            # If there was a genuine TypeError
            if required_args is not None and len(args) >= required_args:
                raise

            # If we only need one more argument
            if (required_args is not None and required_args - len(args) == 1):
                if kwargs:
                    return partial(self.func, *args, **kwargs)
                else:
                    return partial(self.func, *args)

            return curry(self.func, *args, **kwargs)


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
        spec = inspect.getargspec(func)
        may_have_kwargs = bool(not spec or spec.keywords or spec.defaults)
        # Is unary function (single arg, no variadic argument or keywords)?
        is_unary = (spec and spec.varargs is None and not may_have_kwargs
                    and len(spec.args) == 1)
    except TypeError:
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


def juxt(*funcs):
    """
    Creates a function that calls several functions with the same arguments.

    Takes several functions and returns a function that applies its arguments
    to each of those functions then returns a sequence of the results.

    Name comes from juxtaposition: the fact of two things being seen or placed
    close together with contrasting effect.

    >>> inc = lambda x: x + 1
    >>> double = lambda x: x * 2
    >>> list(juxt(inc, double)(10))
    [11, 20]
    >>> list(juxt([inc, double])(10))
    [11, 20]
    """
    if len(funcs) == 1 and not callable(funcs[0]):
        funcs = tuple(funcs[0])

    def juxt_inner(*args, **kwargs):
        return (func(*args, **kwargs) for func in funcs)
    return juxt_inner


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
