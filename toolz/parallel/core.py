from toolz import partition_all

chunksize = 4

def fold(binop, seq, default):
    seq = list(seq)
    if len(seq) < chunksize:
        return reduce(binop, seq, default)
    else:
        chunks = partition_all(chunksize, seq)
        results = map(lambda s: reduce(binop, s, default), chunks)
        return fold(binop, results, default)

