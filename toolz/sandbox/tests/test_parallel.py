from toolz.sandbox.parallel import fold
from toolz import reduce
from operator import add


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
