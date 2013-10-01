from functools import reduce
import itertools


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
    >>> thread_first(1, (add, 4), (pow, 2))  # pow(add(4, 1), 2)
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
            fn, args = form[0], form[1:]
            args = (val,) + args
            return fn(*args)
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
    >>> thread_last(1, (add, 4), (pow, 2))  # pow(2, add(1, 4))
    32

    So in general
        thread_last(x, f, (g, y, z))
    expands to
        g(y, z, f(x))

    >>> def even(x): return x % 2 == 0
    >>> list(thread_last([1, 2, 3], (map, inc), (filter, even)))
    [2, 4]

    See Also:
        thread_first
    """
    def evalform_back(val, form):
        if callable(form):
            return form(val)
        if isinstance(form, tuple):
            fn, args = form[0], form[1:]
            args = args + (val,)
            return fn(*args)
    return reduce(evalform_back, forms, val)


def hashable(x):
    try:
        hash(x)
        return True
    except TypeError:
        return False


def memoize(f, cache=None):
    """ Cache a function's result for speedy future evaluation

    Considerations:
        Trades memory for speed
        Only use on pure functions

    >>> def add(x, y):  return x + y
    >>> add = memoize(add)

    Or use as a decorator

    >>> @memoize
    ... def add(x, y):
    ...     return x + y
    """
    if cache == None:
        cache = {}

    def memof(*args):
        if not hashable(args):
            return f(*args)
        elif args in cache:
            return cache[args]
        else:
            result = f(*args)
            cache[args] = result
            return result
    memof.__name__ = f.__name__
    memof.__doc__ = f.__doc__
    return memof


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
    """
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
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
        kwargs = {}
        kwargs.update(self.kwargs)
        kwargs.update(_kwargs)
        try:
            return self.func(*args, **kwargs)
        except TypeError:
            return curry(self.func, *args, **kwargs)


def compose(*funcs):
    """ Compose functions to operate in series.

    Returns a function that applies other functions in sequence.

    Functions are applied from right to left so that
    ``compose(f, g, h)(x, y)`` is the same as ``f(g(h(x, y)))``.

    If no arguments are provided, the identity function (f(x) = x) is returned.

    >>> inc = lambda i: i + 1
    >>> compose(str, inc)(3)
    '4'
    """
    if not funcs:
        return identity
    if len(funcs) == 1:
        return funcs[0]
    else:
        fns = list(reversed(funcs))

        def composed(*args, **kwargs):
            ret = fns[0](*args, **kwargs)
            for f in fns[1:]:
                ret = f(ret)
            return ret

        return composed
