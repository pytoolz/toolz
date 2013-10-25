from toolz.functoolz import thread_first, thread_last, memoize, curry, compose
from operator import add, mul
from toolz.utils import raises

import itertools


def iseven(x):
    return x % 2 == 0


def isodd(x):
    return x % 2 == 1


def inc(x):
    return x + 1


def double(x):
    return 2 * x


def test_thread_first():
    assert thread_first(2) == 2
    assert thread_first(2, inc) == 3
    assert thread_first(2, inc, inc) == 4
    assert thread_first(2, double, inc) == 5
    assert thread_first(2, (add, 5), double) == 14


def test_thread_last():
    assert list(thread_last([1, 2, 3], (map, inc), (filter, iseven))) == [2, 4]


def test_memoize():
    fn_calls = [0]  # Storage for side effects

    def f(x, y):
        """ A docstring """
        fn_calls[0] += 1
        return x + y
    mf = memoize(f)

    assert mf(2, 3) == mf(2, 3)
    assert fn_calls == [1]  # function was only called once
    assert mf.__doc__ == f.__doc__


def test_curry_simple():
    cmul = curry(mul)
    double = cmul(2)
    assert callable(double)
    assert double(10) == 20


def test_curry_kwargs():
    def f(a, b, c=10):
        return (a + b) * c

    f = curry(f)
    assert f(1, 2, 3) == 9
    assert f(1)(2, 3) == 9
    assert f(1, 2) == 30
    assert f(1, c=3)(2) == 9
    assert f(c=3)(1, 2) == 9


def test_curry_passes_errors():
    @curry
    def f(a, b):
        if not isinstance(a, int):
            raise TypeError()
        return a + b

    assert f(1, 2) == 3
    assert raises(TypeError, lambda : f('1', 2))
    assert raises(TypeError, lambda : f('1')(2))
    assert raises(TypeError, lambda : f(1, 2, 3))


def test_curry_docstring():
    def f(x, y):
        """ A docstring """
        return x

    g = curry(f)
    assert g.__doc__ == f.__doc__
    assert str(g) == str(f)


def test_compose():
    assert compose()(0) == 0
    assert compose(inc)(0) == 1
    assert compose(double, inc)(0) == 2
    assert compose(str, iseven, inc, double)(3) == "False"
    assert compose(str, add)(1, 2) == '3'

    def f(a, b, c=10):
        return (a + b) * c

    assert compose(str, inc, f)(1, 2, c=3) == '10'
