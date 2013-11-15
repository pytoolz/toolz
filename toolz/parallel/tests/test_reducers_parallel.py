import toolz.parallel.reducers as r
from toolz.parallel.core import fold
from toolz import curry, compose

import dill
import pathos

from operator import add

def test_basic():
    p = pathos.multiprocessing.Pool(4)
    data = range(10)
    data = r.filter(lambda x: x % 2 == 0, data)
    data = r.map(lambda x: x**2, data)
    assert data.fn(add)(0, 4) == 16
    assert data.fn(add)(0, 3) == 0

    assert fold(add, data, 0, map=map) == \
                sum(x**2 for x in range(10) if x % 2 == 0)
    assert fold(add, data, 0, map=p.map) == \
                sum(x**2 for x in range(10) if x % 2 == 0)


def test_dill_compose():
    p = pathos.multiprocessing.Pool(4)
    inc = curry(add)(1)
    assert dill.loads(dill.dumps(compose(inc, inc)))(1) == 3
    assert list(p.map(compose(inc, inc), (1, 2, 3))) == [3, 4, 5]

