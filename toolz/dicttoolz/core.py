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


def fnone(f, default):
    """ Returns a version of f able to accept None as its first parameter.

    If `g` is the returned function then:
    -- g(x) == f(default) if x is None
    -- g(x) == f(x) if x is not None

    >>> inc = lambda x: x+1
    >>> fnone(inc, default=-1)(None)
    0
    >>> assert fnone(inc, default=-1)(1) == inc(1)

    >>> fnone(sorted, default=[])(None)
    []
    >>> assert fnone(sorted, default=[])([5, 1, 2]) == sorted([5, 1, 2])

    See also:
        dictoolz.update_in
    """
    def None_safe(x):
        if x is None:
            return f(default)
        else:
            return f(x)
    # temporary hack for Python 2/3 compatibilty
    #try:
    #    None_safe.__qualname__ = 'None_safe_' + f.__qualname__
    #except AttributeError:
    #    None_safe.__name__ = 'None_safe_' + f.__name__
    return None_safe


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

    If any of the keys are not present in d, update_in recursively creates
    nested empty dictionaries to the depth specified by the keys with the
    innermost value set to f(None). For this reason care must be taken to
    ensure that f(None) returns a meaningful value.

    >>> update_in({}, [0, 1, 2, 3], lambda x: x)
    {0: {1: {2: {3: None}}}}

    >>> update_in({}, [0, 1, 2, 3], inc)
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'

    >>> update_in({}, [0, 1, 2, 3], fnone(inc, default=-1))
    {0: {1: {2: {3: 0}}}}

    See Also:
        dictoolz.fnone
    """
    assert len(keys) > 0
    k, ks = keys[0], keys[1:]
    if ks:
        return assoc(d, k, update_in(d.get(k, {}), ks, f))
    else:
        return assoc(d, k, f(d.get(k, None)))
