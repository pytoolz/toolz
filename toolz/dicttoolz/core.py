def merge(*dicts, **kwargs):
    """ Merge a collection of dictionaries

    >>> merge({1: 'one'}, {2: 'two'}, {3: 'three'})
    {1: 'one', 2: 'two', 3: 'three'}

    Later dictionaries have precedence

    >>> merge({1: 2, 3: 4}, {3: 3, 4: 4})
    {1: 2, 3: 3, 4: 4}

    Merge can also be given an iterable of dictionaries

    >>> dicts = ({1: 'one'}, {2: 'two'}, {3: 'three'})
    >>> merge(dicts)
    {1: 'one', 2: 'two', 3: 'three'}
    """
    func = kwargs.get('func', None)

    if (len(dicts) == 1 and not isinstance(dicts[0], dict)):
        dicts = dicts[0]

    if not func:
        rv = dict()
        for d in dicts:
            rv.update(d)
        return rv
    else:
        keys = tuple(set((k for d in dicts for k in d)))
        values = tuple(func([d[k] for d in dicts if k in d])
                                 for k in keys)
        return dict(zip(keys, values))


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
