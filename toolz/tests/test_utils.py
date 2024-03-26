from toolz.utils import raises


def test_raises() -> None:
    assert raises(ZeroDivisionError, lambda: 1 / 0)
    assert not raises(ZeroDivisionError, lambda: 1)
