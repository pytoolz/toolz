from toolz import partition_all, reduce, count
from toolz.parallel.reducers import Reducible


chunksize = 4


def fold(binop, coll, default, map=map):
    if isinstance(coll, Reducible):
        combine = binop
        binop = coll.fn(binop)
        coll = coll.coll
    else:
        combine = binop
    print "Entering Fold with coll: ", coll
    coll = list(coll)  # TODO: Support laziness
    if len(coll) < chunksize:
        return reduce(binop, coll, default)
    else:
        chunks = partition_all(chunksize, coll)
        results = list(map(lambda chunk: reduce(binop, chunk, default),
            chunks))
        return fold(combine, results, default, map=map)


def filter(pred, coll, map=map):
    results = map(lambda x: (pred(x), x), coll)
    return [x for p, x in results if p]
