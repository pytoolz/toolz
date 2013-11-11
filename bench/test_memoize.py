from toolz import memoize


def test_memoize_no_kwargs():
    @memoize
    def f(x):
        return x

    for i in range(100000):
        f(3)
