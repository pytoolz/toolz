from toolz.utils import raises, no_default


def test_raises():
    assert raises(ZeroDivisionError, lambda: 1 / 0)
    assert not raises(ZeroDivisionError, lambda: 1)


def test_no_default_singleton():
    assert raises(TypeError, type(no_default))


def test_no_default_repr():
    assert str(no_default) == repr(no_default) == '<object no_default>'
