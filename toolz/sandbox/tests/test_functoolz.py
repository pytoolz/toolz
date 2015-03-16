from toolz.sandbox.functoolz import pipeseq
from toolz import pipe

def isodd(x):
    return x % 2 == 1

def inc(x):
    return x + 1

def triple(x):
    return 3 * x

def test_pipeseq():

    assert list(pipeseq([0, 1, 2], inc)) == [1, 2, 3]
    assert list(pipeseq(range(10))) == list(range(10))
    assert pipe(10, range, pipeseq, list) == pipe(10, range, list)

    assert list(pipeseq([3, -2, 7], inc, triple, isodd, str)) == ['False',
                                                                  'True',
                                                                  'False']
