from toolz import partition_all, partial
from toolz import reduce as core_reduce

# map is presumed parallel

chunksize = 4

def mpmap(p, func, seq):
    if hasattr(func, 'args') and hasattr(func, 'keywords'):
        seq = [func.args + (item,) for item in seq]
        keywords = func.keywords
        func = func.func
    else:
        seq = ((item,) for item in seq)
        keywords = {}

    if keywords:
        results = [p.apply_async(func, args, keywords) for args in seq]
    else:
        results = [p.apply_async(func, args) for args in seq]


    return map(lambda x: x.get(), results)


def reduce(binop, initial, coll):
    return core_reduce(binop, coll, initial)


def fold(binop, seq, default, map=map):
    seq = list(seq)
    if len(seq) < chunksize:
        return core_reduce(binop, seq, default)
    else:
        chunks = partition_all(chunksize, seq)
        results = map(partial(reduce, binop, default), chunks)
        return fold(binop, results, default)


def filter(pred, seq, map=map):
    results = map(lambda x: (pred(x), x), seq)
    return [x for p, x in results if p]
