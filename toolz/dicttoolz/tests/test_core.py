from toolz.utils import raises
from toolz.dicttoolz import (merge, merge_with, valmap, keymap, update_in,
        assoc, keyfilter, valfilter)


inc = lambda x: x + 1


even = lambda i: i % 2 == 0


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


def test_valfilter():
    assert valfilter(even, {1: 2, 2: 3}) == {1: 2}


def test_keyfilter():
    assert keyfilter(even, {1: 2, 2: 3}) == {2: 3}


def test_assoc():
    assert assoc({}, "a", 1) == {"a": 1}
    assert assoc({"a": 1}, "a", 3) == {"a": 3}
    assert assoc({"a": 1}, "b", 3) == {"a": 1, "b": 3}

    # Verify immutability:
    d = {'x': 1}
    oldd = d
    assoc(d, 'x', 2)
    assert d is oldd


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
