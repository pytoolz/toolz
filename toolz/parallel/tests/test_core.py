from toolz.parallel.core import fold, mpmap
from toolz.parallel.core import filter as pfilter
import operator as op
from functools import partial

iseven = lambda x: x % 2 == 0

def test_fold():
    print fold(op.add, range(10), 0)
    print reduce(op.add, range(10), 0)
    assert fold(op.add, range(10), 0) == reduce(op.add, range(10), 0)


def test_filter():
    assert list(filter(iseven, range(10))) == list(filter(iseven, range(10)))


def test_fold_multiprocessing():
    from multiprocessing import Pool
    p = Pool(4)
    assert fold(op.add, range(10), 0, map=partial(mpmap, p)) == sum(range(10))
