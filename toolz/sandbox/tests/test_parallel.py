from toolz.sandbox.parallel import fold
from toolz import reduce
from operator import add
from pickle import dumps, loads

# is comparison will fail between this and no_default
no_default2 = loads(dumps('__no__default__'))


def test_fold():
    assert fold(add, range(10), 0) == reduce(add, range(10), 0)
    assert fold(add, range(10), 0, chunksize=2) == reduce(add, range(10), 0)
    assert fold(add, range(10)) == fold(add, range(10), 0)

    def setadd(s, item):
        s = s.copy()
        s.add(item)
        return s

    assert fold(setadd, [1, 2, 3], set()) == set((1, 2, 3))
    assert (fold(setadd, [1, 2, 3], set(), chunksize=2, combine=set.union)
            == set((1, 2, 3)))

    assert fold(add, range(10), default=no_default2) == fold(add, range(10))
