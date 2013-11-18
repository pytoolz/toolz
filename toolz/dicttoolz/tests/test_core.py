from toolz.utils import raises
from toolz.dicttoolz import (merge, merge_with, valmap, keymap, update_in, assoc, 
                             fnone)


inc = lambda x: x + 1


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


def test_assoc():
    assert assoc({}, "a", 1) == {"a": 1}
    assert assoc({"a": 1}, "a", 3) == {"a": 3}
    assert assoc({"a": 1}, "b", 3) == {"a": 1, "b": 3}

    # Verify immutability:
    d = {'x': 1}
    oldd = d
    assoc(d, 'x', 2)
    assert d is oldd


def test_fnone():
    inc = lambda x: x+1
    assert fnone(str, '')(None) == ''
    assert raises(TypeError, fnone(str, None)(None))
    assert update_in({}, [0, 1], fnone(inc, -1)) == {0: {1: 0}}
    assert raises(TypeError,
                  lambda: update_in({}, [0, 1], inc, -1))


def test_update_in():
    assert update_in({"a": 0}, ["a"], inc) == {"a": 1}
    assert update_in({"a": 0, "b": 1}, ["b"], str) == {"a": 0, "b": "1"}
    assert (update_in({"t": 1, "v": {"a": 0}}, ["v", "a"], inc) ==
            {"t": 1, "v": {"a": 1}})
    # Handle one missing key.
    assert update_in({}, ["z"], str) == {"z": "None"}
    # Same semantics as Clojure for multiple missing keys, ie. recursively
    # create nested empty dictionaries to the depth specified by the
    # keys with the innermost value set to f(None).
    assert (update_in({}, [0, 1], lambda x: 0 if (x is None) else inc(x)) ==
            {0: {1: 0}})
    assert update_in({}, [0, 1], fnone(inc, -1)) == {0: {1: 0}}
    assert update_in({}, [0, 1], fnone(str, "foo")) == {0: {1: "foo"}}
    # check for TypeError when no default value is provided.
    assert raises(TypeError,
                  lambda: update_in({}, [0, 2], inc))

    # Verify immutability:
    d = {'x': 1}
    oldd = d
    update_in(d, ['x'], inc)
    assert d is oldd
