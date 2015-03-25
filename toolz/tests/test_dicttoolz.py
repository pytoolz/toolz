from collections import defaultdict as _defaultdict
from toolz.dicttoolz import (merge, merge_with, valmap, keymap, update_in,
                             assoc, dissoc, keyfilter, valfilter, itemmap,
                             itemfilter)


class defaultdict(_defaultdict):
    def __eq__(self, other):
        return (super(defaultdict, self).__eq__(other) and
                isinstance(other, _defaultdict) and
                self.default_factory == other.default_factory)


def inc(x):
    return x + 1


def iseven(i):
    return i % 2 == 0


def test_merge():
    assert merge({1: 1, 2: 2}, {3: 4}) == {1: 1, 2: 2, 3: 4}


def test_merge_iterable_arg():
    assert merge([{1: 1, 2: 2}, {3: 4}]) == {1: 1, 2: 2, 3: 4}


def test_merge_with():
    dicts = {1: 1, 2: 2}, {1: 10, 2: 20}
    assert merge_with(sum, *dicts) == {1: 11, 2: 22}
    assert merge_with(tuple, *dicts) == {1: (1, 10), 2: (2, 20)}

    dicts = {1: 1, 2: 2, 3: 3}, {1: 10, 2: 20}
    assert merge_with(sum, *dicts) == {1: 11, 2: 22, 3: 3}
    assert merge_with(tuple, *dicts) == {1: (1, 10), 2: (2, 20), 3: (3,)}

    assert not merge_with(sum)


def test_merge_with_iterable_arg():
    dicts = {1: 1, 2: 2}, {1: 10, 2: 20}
    assert merge_with(sum, *dicts) == {1: 11, 2: 22}
    assert merge_with(sum, dicts) == {1: 11, 2: 22}
    assert merge_with(sum, iter(dicts)) == {1: 11, 2: 22}


def test_valmap():
    assert valmap(inc, {1: 1, 2: 2}) == {1: 2, 2: 3}


def test_keymap():
    assert keymap(inc, {1: 1, 2: 2}) == {2: 1, 3: 2}


def test_itemmap():
    assert itemmap(reversed, {1: 2, 2: 4}) == {2: 1, 4: 2}


def test_valfilter():
    assert valfilter(iseven, {1: 2, 2: 3}) == {1: 2}


def test_keyfilter():
    assert keyfilter(iseven, {1: 2, 2: 3}) == {2: 3}


def test_itemfilter():
    assert itemfilter(lambda item: iseven(item[0]), {1: 2, 2: 3}) == {2: 3}
    assert itemfilter(lambda item: iseven(item[1]), {1: 2, 2: 3}) == {1: 2}


def test_assoc():
    assert assoc({}, "a", 1) == {"a": 1}
    assert assoc({"a": 1}, "a", 3) == {"a": 3}
    assert assoc({"a": 1}, "b", 3) == {"a": 1, "b": 3}

    # Verify immutability:
    d = {'x': 1}
    oldd = d
    assoc(d, 'x', 2)
    assert d is oldd


def test_dissoc():
    assert dissoc({"a": 1}, "a") == {}
    assert dissoc({"a": 1, "b": 2}, "a") == {"b": 2}
    assert dissoc({"a": 1, "b": 2}, "b") == {"a": 1}

    # Verify immutability:
    d = {'x': 1}
    oldd = d
    d2 = dissoc(d, 'x')
    assert d is oldd
    assert d2 is not oldd


def test_update_in():
    assert update_in({"a": 0}, ["a"], inc) == {"a": 1}
    assert update_in({"a": 0, "b": 1}, ["b"], str) == {"a": 0, "b": "1"}
    assert (update_in({"t": 1, "v": {"a": 0}}, ["v", "a"], inc) ==
            {"t": 1, "v": {"a": 1}})
    # Handle one missing key.
    assert update_in({}, ["z"], str, None) == {"z": "None"}
    assert update_in({}, ["z"], inc, 0) == {"z": 1}
    assert update_in({}, ["z"], lambda x: x+"ar", default="b") == {"z": "bar"}
    # Same semantics as Clojure for multiple missing keys, ie. recursively
    # create nested empty dictionaries to the depth specified by the
    # keys with the innermost value set to f(default).
    assert update_in({}, [0, 1], inc, default=-1) == {0: {1: 0}}
    assert update_in({}, [0, 1], str, default=100) == {0: {1: "100"}}
    assert (update_in({"foo": "bar", 1: 50}, ["d", 1, 0], str, 20) ==
            {"foo": "bar", 1: 50, "d": {1: {0: "20"}}})
    # Verify immutability:
    d = {'x': 1}
    oldd = d
    update_in(d, ['x'], inc)
    assert d is oldd


def test_factory():
    assert merge(defaultdict(int, {1: 2}), {2: 3}) == {1: 2, 2: 3}
    assert (merge(defaultdict(int, {1: 2}), {2: 3},
                  factory=lambda: defaultdict(int)) ==
            defaultdict(int, {1: 2, 2: 3}))
    assert not (merge(defaultdict(int, {1: 2}), {2: 3},
                      factory=lambda: defaultdict(int)) == {1: 2, 2: 3})
