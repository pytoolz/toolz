from toolz.utils import raises
from toolz.dicttoolz import merge, merge_with, valmap, keymap, update_in, assoc


inc = lambda x: x + 1


def test_merge():
    assert merge({1: 1, 2: 2}, {3: 4}) == {1: 1, 2: 2, 3: 4}


def test_merge_with():
    dicts = {1: 1, 2: 2}, {1: 10, 2: 20}
    assert merge_with(sum, *dicts) == {1: 11, 2: 22}
    assert merge_with(tuple, *dicts) == {1: (1, 10), 2: (2, 20)}

    dicts = {1: 1, 2: 2, 3: 3}, {1: 10, 2: 20}
    assert merge_with(sum, *dicts) == {1: 11, 2: 22, 3: 3}
    assert merge_with(tuple, *dicts) == {1: (1, 10), 2: (2, 20), 3: (3,)}


def test_valmap():
    assert valmap(inc, {1: 1, 2: 2}) == {1: 2, 2: 3}


def test_keymap():
    assert keymap(inc, {1: 1, 2: 2}) == {2: 1, 3: 2}


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
    assert (update_in({"t": 1,
                       "v": {"a": 0}}, ["v", "a"], inc) ==
            {"t": 1, "v": {"a": 1}})
    # Handle missing element one deep:
    assert update_in({}, ["z"], str) == {"z": "None"}
    # Same semantics as Clojure, raises an error if going deeper than
    # one level into a dict which doesn't have the initial key:
    assert raises(AttributeError,
                  lambda: update_in({}, ["z", "q"], str))

    # Verify immutability:
    d = {'x': 1}
    oldd = d
    update_in(d, ['x'], inc)
    assert d is oldd
