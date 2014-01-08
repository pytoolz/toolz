from toolz import partial, compose


def test_compose_multiprocessing():
    from operator import add, mul
    inc = partial(add, 1)
    double = partial(mul, 2)
    f = compose(double, inc)

    import multiprocessing as mp
    try:
        p = mp.Pool(4)
    except OSError:  # Travis doesn't support multiprocessing trivially
        return

    assert p.map(f, [1, 2, 3, 4], chunksize=1) == [4, 6, 8, 10]
