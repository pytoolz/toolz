from toolz import partition_all, reduce, count
from toolz.parallel.reducers import Reducible  # TODO: this dependency is wrong


chunksize = 4


def fold(binop, coll, default, map=map):
    """ Reduce without guarantee of ordered reduction

    ``binop`` is assumed to be an associative operator

    This allows us to leverage a parallel map to perform reductions in parallel

    See Also:
        toolz.parallel.reducers
    """
    if isinstance(coll, Reducible):  # TODO: this dependency is wrong
        combine = binop
        binop = coll.fn(binop)
        coll = coll.coll
    else:
        combine = binop

    coll = list(coll)  # TODO: Support laziness
    if len(coll) < chunksize:
        return reduce(binop, coll, default)
    else:
        chunks = partition_all(chunksize, coll)
        results = list(map(lambda chunk: reduce(binop, chunk, default),
            chunks))
        return fold(combine, results, default, map=map)


def filter(pred, coll, map=map):
    """ Implementation of filter that depends on map

    So that a parallel map can form a parallel filter
    """
    results = map(lambda x: (pred(x), x), coll)
    return [x for p, x in results if p]
