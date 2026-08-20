import pytest
from toolz import tail


def test_tail_zero_returns_empty():
    """Test that tail(0, seq) returns empty sequence consistently across iterable types."""
    # Test with list (sliceable)
    assert list(tail(0, [10, 20, 30])) == []

    # Test with tuple (sliceable)
    assert tuple(tail(0, (10, 20, 30))) == ()

    # Test with iterator (non-sliceable)
    assert tuple(tail(0, iter([10, 20, 30]))) == ()

    # Test with string (sliceable)
    assert tail(0, "abc") == ""

    # Consistency check: all should be empty
    assert list(tail(0, [1, 2, 3, 4, 5])) == []
