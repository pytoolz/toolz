def merge(*dicts):
    """ Merge a collection of dictionaries

    >>> merge({1: 'one'}, {2: 'two'})
    {1: 'one', 2: 'two'}

    Later dictionaries have precedence

    >>> merge({1: 2, 3: 4}, {3: 3, 4: 4})
    {1: 2, 3: 3, 4: 4}
    """
    rv = dict()
    for d in dicts:
        rv.update(d)
    return rv


def valmap(fn, d):
    """ Apply function to values of dictionary

    >>> bills = {"Alice": [20, 15, 30], "Bob": [10, 35]}
    >>> valmap(sum, bills)  # doctest: +SKIP
    {'Alice': 65, 'Bob': 45}

    See Also:
        keymap
    """
    return dict(zip(d.keys(), map(fn, d.values())))


def keymap(fn, d):
    """ Apply function to keys of dictionary

    >>> bills = {"Alice": [20, 15, 30], "Bob": [10, 35]}
    >>> keymap(str.lower, bills)  # doctest: +SKIP
    {'alice': [20, 15, 30], 'bob': [10, 35]}

    See Also:
        valmap
    """
    return dict(zip(map(fn, d.keys()), d.values()))


def assoc(d, q, r):
    """
    Return a new dict with q: r added in

    New dict has d["q"] set to r. Do not modify the initial dict.

    >>> assoc({"z": 1}, "z", 2)
    {'z': 2}
    >>> assoc({"z": 1}, "b", 3)   # doctest: +SKIP
    {'z': 1, 'b': 3}
    """
    return dict(list(d.items()) + [(q, r)])


def update_in(dikt, keys, f):
    """ Immutably update value in a (potentially) nested dictionary.

    keys is a list or tuple or anything which supports indexing, which
    gives the "location" of the value in dikt; f is the function which
    operates on the value to produce an updated value.

    Translated from Clojure,
    http://clojuredocs.org/clojure_core/1.2.0/clojure.core/update-in

    >>> update_in({"x": {"a": 33}}, ["x", "a"], str)
    {'x': {'a': '33'}}
    """
    assert len(keys) > 0
    if len(keys) == 1:
        return assoc(dikt, keys[0], f(dikt.get(keys[0], None)))
    else:
        return assoc(dikt, keys[0], update_in(dikt.get(keys[0], None),
                                              keys[1:], f))
