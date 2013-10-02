import itertools
from .core import groupby, frequencies, second
from ..functoolz import compose
from ..compatibility import map


def countby(func, seq):
    """ Count elements of a collection by a key function

    >>> countby(len, ['cat', 'mouse', 'dog'])
    {3: 2, 5: 1}

    >>> def even(x): return x % 2 == 0
    >>> countby(even, [1, 2, 3])  # doctest:+SKIP
    {True: 1, False: 2}

    See Also:
        groupby
    """
    return frequencies(map(func, seq))


def partitionby(f, s):
    """ Partition a sequence according to a function

    Partition `s` into a sequence of lists such that every time `f(s)`
    changes, a new list is started and items are collected into that
    list.

    Note: mapping `compose(list, second)` is required to make this
    both Python 2 and 3 compatible (Python 3 works without the
    application of `list`).

    >>> is_space = lambda c: c == " "
    >>> list(partitionby(is_space, "I have spaces"))
    [['I'], [' '], ['h', 'a', 'v', 'e'], [' '], ['s', 'p', 'a', 'c', 'e', 's']]

    >>> is_large = lambda x: x > 10
    >>> list(partitionby(is_large, [1, 2, 1, 99, 88, 33, 99, -1, 5]))
    [[1, 2, 1], [99, 88, 33, 99], [-1, 5]]

    See also:
        partition
        groupby
    """
    return map(compose(list, second), itertools.groupby(s, key=f))
