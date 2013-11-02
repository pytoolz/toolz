import itertools
from toolz import first, second

iters = itertools.imap(iter, [(1, 2) for i in range(1000000)])

def test_first_iter():
    for p in iters:
        first(p)


def test_second_iter():
    for p in iters:
        second(p)
