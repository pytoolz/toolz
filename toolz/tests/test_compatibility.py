import pytest


def test_compat_warn():
    with pytest.warns(DeprecationWarning):
        import toolz.compatibility
