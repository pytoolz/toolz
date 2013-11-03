def merge(*dicts):
    """ Merge a collection of dictionaries

    >>> merge({1: 'one'}, {2: 'two'})
    {1: 'one', 2: 'two'}

    Later dictionaries have precedence

    >>> merge({1: 2, 3: 4}, {3: 3, 4: 4})
    {1: 2, 3: 3, 4: 4}

    See Also:
        merge_with
    """
    if len(dicts) == 1 and not isinstance(dicts[0], dict):
        dicts = dicts[0]

    rv = dict()
    for d in dicts:
        rv.update(d)
    return rv


def merge_with(fn, *dicts):
    """ Merge dictionaries and apply function to combined values

    A key may occur in more than one dict, and all values mapped from the key
    will be passed to the function as a list, such as fn([val1, val2, ...]).

    >>> merge_with(sum, {1: 1, 2: 2}, {1: 10, 2: 20})
    {1: 11, 2: 22}

    >>> merge_with(first, {1: 1, 2: 2}, {2: 20, 3: 30})  # doctest: +SKIP
    {1: 1, 2: 2, 3: 30}

    See Also:
        merge
    """
    if len(dicts) == 1 and not isinstance(dicts[0], dict):
        dicts = dicts[0]

    result = dict()
    for d in dicts:
        for k, v in d.items():
            try:
                result[k].append(v)
            except:
                result[k] = [v]
    return dict((k, fn(v)) for k, v in result.items())


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


def assoc(d, key, value):
    """
    Return a new dict with new key value pair

    New dict has d[key] set to value. Does not modify the initial dictionary.

    >>> assoc({'x': 1}, 'x', 2)
    {'x': 2}
    >>> assoc({'x': 1}, 'y', 3)   # doctest: +SKIP
    {'x': 1, 'y': 3}
    """
    d = d.copy()
    d[key] = value
    return d


def update_in(d, keys, f):
    """ Update value in a (potentially) nested dictionary

    inputs:
    d - nested dictionary on which to operate
    keys - list or tuple giving the location of the value to be changed in d
    f - function to operate on that value

    Returns a copy of the original rather than mutating it.

    >>> inc = lambda x: x + 1
    >>> update_in({'a': 0}, ['a'], inc)
    {'a': 1}

    >>> transaction = {'name': 'Alice',
    ...                'purchase': {'items': ['Apple', 'Orange'],
    ...                             'costs': [0.50, 1.25]},
    ...                'credit card': '5555-1234-1234-1234'}
    >>> update_in(transaction, ['purchase', 'costs'], sum) # doctest: +SKIP
    {'credit card': '5555-1234-1234-1234',
     'name': 'Alice',
     'purchase': {'costs': 1.75, 'items': ['Apple', 'Orange']}}
    """
    assert len(keys) > 0
    if len(keys) == 1:
        return assoc(d, keys[0], f(d.get(keys[0], None)))
    else:
        return assoc(d, keys[0], update_in(d.get(keys[0], None),
                                           keys[1:], f))
