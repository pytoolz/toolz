import itertools
from toolz import first, second


def test_first_iter():
    iters = map(iter, [(1, 2) for i in range(1000000)])
    for p in iters:
        first(p)


def test_second_iter():
    iters = map(iter, [(1, 2) for i in range(1000000)])
    for p in iters:
        second(p)
