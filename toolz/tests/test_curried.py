import toolz
from toolz.curried import take, first, merge_with


def test_take():
    assert list(take(2)([1, 2, 3])) == [1, 2]


def test_first():
    assert first is toolz.itertoolz.core.first


def test_merge_with():
    assert merge_with(sum)({1: 1}, {1: 2}) == {1: 3}
