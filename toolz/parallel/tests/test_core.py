from toolz.parallel.core import fold
import operator as op

def test_fold():
    print fold(op.add, range(10), 0)
    print reduce(op.add, range(10), 0)
    assert fold(op.add, range(10), 0) == reduce(op.add, range(10), 0)
