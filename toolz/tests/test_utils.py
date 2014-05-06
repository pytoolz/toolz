from toolz.utils import raises, consume


def test_raises():
    assert raises(ZeroDivisionError, lambda: 1 / 0)
    assert not raises(ZeroDivisionError, lambda: 1)


def test_consume():
    data = [1, 2, 3, 4]
    it = iter(data)
    assert consume(it) is None
    assert raises(StopIteration, lambda: next(it))
    assert consume(data) is None
