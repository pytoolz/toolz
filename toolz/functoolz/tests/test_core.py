from toolz.functoolz import (accumulate, iterate, remove,
                             thread_first, thread_last,
                             memoize, curry, comp)
from toolz.itertoolz import groupby, identity
from operator import add, mul

import itertools


def even(x):
    return x % 2 == 0


def odd(x):
    return x % 2 == 1


def inc(x):
    return x + 1


def double(x):
    return 2 * x


def test_remove():
    assert list(remove(even, range(5))) == list(filter(odd, range(5)))


def test_thread_first():
    assert thread_first(2) == 2
    assert thread_first(2, inc) == 3
    assert thread_first(2, inc, inc) == 4
    assert thread_first(2, double, inc) == 5
    assert thread_first(2, (add, 5), double) == 14


def test_thread_last():
    assert list(thread_last([1, 2, 3], (map, inc), (filter, even))) == [2, 4]


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


def test_comp():
    assert comp()(0) == 0
    assert comp(inc)(0) == 1
    assert comp(double, inc)(0) == 2
    assert comp(str, even, inc, double)(3) == "False"
    assert groupby(comp(), range(3)) == {0: [0], 1: [1], 2: [2]}
    assert groupby(comp(identity,
                        identity,
                        even), range(3)) == {True: [0, 2], False: [1]}
    small = lambda x: x < 10
    square = lambda x: x * x
    assert groupby(comp(small,
                        square), range(10)) == {True: [0, 1, 2, 3],
                                                False: [4, 5, 6, 7, 8, 9]}


def test_iterate():
    assert list(itertools.islice(iterate(inc, 0), 0, 5)) == [0, 1, 2, 3, 4]


def test_accumulate():
    assert list(accumulate(add, [1, 2, 3, 4, 5])) == [1, 3, 6, 10, 15]
    assert list(accumulate(mul, [1, 2, 3, 4, 5])) == [1, 2, 6, 24, 120]
