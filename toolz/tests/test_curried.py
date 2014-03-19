import toolz
import toolz.curried
from toolz.curried import take, first, second, sorted, merge_with, reduce
from operator import add


def test_take():
    assert list(take(2)([1, 2, 3])) == [1, 2]


def test_first():
    assert first is toolz.itertoolz.core.first


def test_merge_with():
    assert merge_with(sum)({1: 1}, {1: 2}) == {1: 3}


def test_sorted():
    assert sorted(key=second)([(1, 2), (2, 1)]) == [(2, 1), (1, 2)]


def test_reduce():
    assert reduce(add)((1, 2, 3)) == 6


def test_module_name():
    assert toolz.curried.__name__ == 'toolz.curried'
