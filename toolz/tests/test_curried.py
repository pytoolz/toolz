import toolz
from toolz.curried import (take, first, second, sorted, merge_with, lmap,
                           should_curry)


def test_take():
    assert list(take(2)([1, 2, 3])) == [1, 2]


def test_first():
    assert first is toolz.itertoolz.core.first


def test_merge_with():
    assert merge_with(sum)({1: 1}, {1: 2}) == {1: 3}


def test_sorted():
    assert sorted(key=second)([(1, 2), (2, 1)]) == [(2, 1), (1, 2)]


def test_should_curry():
    assert should_curry(toolz.map)
    assert should_curry(toolz.lmap)
    assert should_curry(toolz.groupby)
    assert should_curry(toolz.take)
    assert not should_curry(toolz.first)


def test_lmap():
    assert lmap(lambda x: x + 1)([1]) == [2]
