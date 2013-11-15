from toolz import partition_all, reduce, count
from toolz.parallel.reducers import Reducible  # TODO: this dependency is wrong


chunksize = 4


def fold(binop, coll, default, map=map, chunksize=chunksize):
    """ Reduce without guarantee of ordered reduction

    ``binop`` is assumed to be an associative operator.  This allows us to
    leverage a parallel map to perform reductions in parallel.

    inputs:
        # The first inputs are almost the same as reduce
        binop: associative binary operator like add or mul
        coll: a collection or sequence
        default: an identity element like 0 for add or 1 for mul
        # The optional map input is new
        map: an implementation of ``map``.  This may be parallel.

    Fold chunks up the collection into blocks of size ``chunksize`` and then
    feeds each of these to calls to `builtin.reduce`.  This work is distributed
    with a call to ``map``, gathered back and then refolded to finish the
    computation.  In this way ``fold`` specifies only how to chunk up data but
    leaves the distribution of this work to an externally provided ``map``
    function.  This function can be sequential or rely on multithreading,
    multiprocessing, or even distributed solutions.

    If ``map`` intends to serialize functions it should be prepared to accept
    and serialize lambdas.  Note that the standard ``pickle`` module fails
    here.

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
