from toolz.parallel.reducers import *
from operator import add, mul
from toolz import identity


def iseven(n):
    return n % 2 == 0


def square(x):
    return x ** 2


def test_reduce():
    assert reduce(add, range(10), 0) == sum(range(10))


L = list(range(10))


def test_Reducible():
    red = Reducible(identity, L)
    assert reduce(add, red, 0) == core_reduce(add, L, 0)


def test_map():
    L2 = map(square, L)
    assert L2.fn(add)(10, 3) == 10 + 3**2
    assert reduce(add, map(square, L), 0) == sum([x**2 for x in range(10)])


def test_filter():
    red2 = filter(iseven, L)
    assert red2.fn(add)(10, 3) == 10
    assert red2.fn(add)(10, 4) == 14
    assert reduce(add, filter(iseven, L), 0) == sum([x for x in range(10)
                                                       if iseven(x)])

