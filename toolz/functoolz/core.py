from functools import reduce, partial
import itertools
import inspect


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
            fn, args = form[0], form[1:]
            args = args + (val,)
            return fn(*args)
    return reduce(evalform_back, forms, val)


def memoize(f, cache=None):
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
    """
    if cache is None:
        cache = {}

    try:
        spec = inspect.getargspec(f)
        if spec and not spec.keywords and not spec.defaults:
            may_have_kwargs = False
        else:
            may_have_kwargs = True
    except TypeError:
        may_have_kwargs = True

    def memof(*args, **kwargs):
        try:
            if may_have_kwargs:
                key = (args, frozenset(kwargs.items()))
            else:
                key = args
            in_cache = key in cache
        except TypeError:
            raise TypeError("Arguments to memoized function must be hashable")

        if in_cache:
            return cache[key]
        else:
            result = f(*args, **kwargs)
            cache[key] = result
            return result

    try:
        memof.__name__ = f.__name__
    except AttributeError:
        pass
    memof.__doc__ = f.__doc__
    return memof


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
        except TypeError as e:
            required_args = _num_required_args(self.func)

            # If there was a genuine TypeError
            if required_args is not None and len(args) >= required_args:
                raise e

            # If we only need one more argument
            if (required_args is not None and required_args - len(args) == 1):
                if kwargs:
                    return partial(self.func, *args, **kwargs)
                else:
                    return partial(self.func, *args)

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

    See Also:
        pipe
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


def pipe(data, *functions):
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
    for func in functions:
        data = func(data)
    return data
