from toolz import partition_all

# map is presumed parallel

chunksize = 4

def fold(binop, seq, default, map=map):
    seq = list(seq)
    if len(seq) < chunksize:
        return reduce(binop, seq, default)
    else:
        chunks = partition_all(chunksize, seq)
        results = map(lambda s: reduce(binop, s, default), chunks)
        return fold(binop, results, default)


def filter(pred, seq, map=map):
    results = map(lambda x: (pred(x), x), seq)
    return [x for p, x in results if p]
