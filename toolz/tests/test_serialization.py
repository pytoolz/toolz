from toolz import *
import pickle


def test_compose():
    f = compose(str, sum)
    g = pickle.loads(pickle.dumps(f))
    assert f((1, 2)) == g((1, 2))


def test_curry():
    f = curry(map)(str)
    g = pickle.loads(pickle.dumps(f))
    assert list(f((1, 2, 3))) == list(g((1, 2, 3)))


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
