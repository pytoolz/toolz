"""
Reducers
========

Applying functions onto binops rather than functions onto sequences

Inspired by clojure.core.reducers

See the following explanatory blogpost
http://clojure.com/blog/2012/05/08/reducers-a-library-and-model-for-collection-processing.html

"""

from toolz import reduce as core_reduce
from toolz import compose

class Reducible(object):
    __slots__ = ['fn', 'coll']
    def __init__(self, fn, coll):
        self.fn = fn
        self.coll = coll

    def _reduce(self, binop, init):
        return reduce(self.fn(binop), self.coll, init)


def reducer(xf, coll):
    if isinstance(coll, Reducible):
        return Reducible(compose(xf, coll.fn), coll.coll)
    else:
        return Reducible(xf, coll)


def map(fn, coll):
    def refold(binop):
        def new_binop(acc, x):
            return binop(acc, fn(x))
        return new_binop
    return reducer(refold, coll)


def filter(pred, coll):
    def refold(binop):
        def newfn(acc, x):
            if pred(x):
                return binop(acc, x)
            else:
                return acc
        return newfn
    return reducer(refold, coll)


def reduce(binop, coll, init):
    if hasattr(coll, '_reduce'):
        return coll._reduce(binop, init)
    else:
        return core_reduce(binop, coll, init)
