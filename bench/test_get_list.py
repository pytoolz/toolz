from toolz import get
from functools import partial

tuples = [(1, 2, 3) for i in range(100000)]

def test_get():
    for tup in tuples:
        get([1, 2], tup)
