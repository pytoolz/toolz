import operator
import copy
from toolz.compatibility import (map, zip, iteritems, iterkeys, itervalues,
                                 reduce)

__all__ = ('merge', 'merge_with', 'valmap', 'keymap', 'valfilter', 'keyfilter',
           'assoc', 'update_in', 'get_in')


no_default = '__no__default__'


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

    rv = {}
    for d in dicts:
        rv.update(d)
    return rv


def merge_with(func, *dicts):
    """ Merge dictionaries and apply function to combined values

    A key may occur in more than one dict, and all values mapped from the key
    will be passed to the function as a list, such as func([val1, val2, ...]).

    >>> merge_with(sum, {1: 1, 2: 2}, {1: 10, 2: 20})
    {1: 11, 2: 22}

    >>> merge_with(first, {1: 1, 2: 2}, {2: 20, 3: 30})  # doctest: +SKIP
    {1: 1, 2: 2, 3: 30}

    See Also:
        merge
    """
    if len(dicts) == 1 and not isinstance(dicts[0], dict):
        dicts = dicts[0]

    result = {}
    for d in dicts:
        for k, v in iteritems(d):
            if k not in result:
                result[k] = [v]
            else:
                result[k].append(v)
    return dict((k, func(v)) for k, v in iteritems(result))


def valmap(func, d):
    """ Apply function to values of dictionary

    >>> bills = {"Alice": [20, 15, 30], "Bob": [10, 35]}
    >>> valmap(sum, bills)  # doctest: +SKIP
    {'Alice': 65, 'Bob': 45}

    See Also:
        keymap
    """
    return dict(zip(iterkeys(d), map(func, itervalues(d))))


def keymap(func, d):
    """ Apply function to keys of dictionary

    >>> bills = {"Alice": [20, 15, 30], "Bob": [10, 35]}
    >>> keymap(str.lower, bills)  # doctest: +SKIP
    {'alice': [20, 15, 30], 'bob': [10, 35]}

    See Also:
        valmap
    """
    return dict(zip(map(func, iterkeys(d)), itervalues(d)))


def valfilter(predicate, d):
    """ Filter items in dictionary by value

    >>> iseven = lambda x: x % 2 == 0
    >>> d = {1: 2, 2: 3, 3: 4, 4: 5}
    >>> valfilter(iseven, d)
    {1: 2, 3: 4}

    See Also:
        keyfilter
        valmap
    """
    rv = {}
    for k, v in iteritems(d):
        if predicate(v):
            rv[k] = v
    return rv


def keyfilter(predicate, d):
    """ Filter items in dictionary by key

    >>> iseven = lambda x: x % 2 == 0
    >>> d = {1: 2, 2: 3, 3: 4, 4: 5}
    >>> keyfilter(iseven, d)
    {2: 3, 4: 5}

    See Also:
        valfilter
        keymap
    """
    rv = {}
    for k, v in iteritems(d):
        if predicate(k):
            rv[k] = v
    return rv


def assoc(d, key, value):
    """
    Return a new dict with new key value pair

    New dict has d[key] set to value. Does not modify the initial dictionary.

    >>> assoc({'x': 1}, 'x', 2)
    {'x': 2}
    >>> assoc({'x': 1}, 'y', 3)   # doctest: +SKIP
    {'x': 1, 'y': 3}
    """
    if isinstance(d, dict):
        return merge(d, {key: value})
    else:
        d = copy.copy(d)
        setattr(d, key, value)
        return d


def update_in(d, keys, func, default=None):
    """ Update value in a (potentially) nested dictionary

    inputs:
    d - dictionary on which to operate
    keys - list or tuple giving the location of the value to be changed in d
    func - function to operate on that value

    If keys == [k0,..,kX] and d[k0]..[kX] == v, update_in returns a copy of the
    original dictionary with v replaced by func(v), but does not mutate the
    original dictionary.

    If k0 is not a key in d, update_in creates nested dictionaries to the depth
    specified by the keys, with the innermost value set to func(default).

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

    >>> # updating a value when k0 is not in d
    >>> update_in({}, [1, 2, 3], str, default="bar")
    {1: {2: {3: 'bar'}}}
    >>> update_in({1: 'foo'}, [2, 3, 4], inc, 0)
    {1: 'foo', 2: {3: {4: 1}}}
    """
    def get(k, d, default):
        if isinstance(d, dict):
            return d.get(k, default)
        else:
            if default is no_default:
                return getattr(d, k)
            else:
                return getattr(d, k, default)

    assert len(keys) > 0
    k, ks = keys[0], keys[1:]
    if ks:
        nested = {} if isinstance(d, dict) else no_default
        val = update_in(get(k, d, nested), ks, func, default)
    else:
        val = func(get(k, d, default))
    return assoc(d, k, val)


def get_in(keys, coll, default=None, no_default=False):
    """
    Returns coll[i0][i1]...[iX] where [i0, i1, ..., iX]==keys.

    If coll[i0][i1]...[iX] cannot be found, returns ``default``, unless
    ``no_default`` is specified, then it raises KeyError or IndexError.

    ``get_in`` is a generalization of ``operator.getitem`` for nested data
    structures such as dictionaries and lists.

    >>> transaction = {'name': 'Alice',
    ...                'purchase': {'items': ['Apple', 'Orange'],
    ...                             'costs': [0.50, 1.25]},
    ...                'credit card': '5555-1234-1234-1234'}
    >>> get_in(['purchase', 'items', 0], transaction)
    'Apple'
    >>> get_in(['name'], transaction)
    'Alice'
    >>> get_in(['purchase', 'total'], transaction)
    >>> get_in(['purchase', 'items', 'apple'], transaction)
    >>> get_in(['purchase', 'items', 10], transaction)
    >>> get_in(['purchase', 'total'], transaction, 0)
    0
    >>> get_in(['y'], {}, no_default=True)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    AttributeError: ... has no attribute 'y'

    See Also:
        itertoolz.get
        operator.getitem
    """
    def get(d, key):
        return d[key] if hasattr(d, '__getitem__') else getattr(d, key)

    try:
        return reduce(get, keys, coll)
    except (KeyError, IndexError, AttributeError, TypeError):
        if no_default:
            raise
        return default
