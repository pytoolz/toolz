import itertools
from .itertoolz import frequencies, pluck, getter
from .functoolz import composed

__all__ = ('countby', 'partitionby', 'collect')


def countby(key, seq):
    """ Count elements of a collection by a key function

    >>> countby(len, ['cat', 'mouse', 'dog'])
    {3: 2, 5: 1}

    >>> def iseven(x): return x % 2 == 0
    >>> countby(iseven, [1, 2, 3])  # doctest:+SKIP
    {True: 1, False: 2}

    See Also:
        groupby
    """
    if not callable(key):
        key = getter(key)
    return frequencies(map(key, seq))


def partitionby(func, seq):
    """ Partition a sequence according to a function

    Partition `s` into a sequence of lists such that, when traversing
    `s`, every time the output of `func` changes a new list is started
    and that and subsequent items are collected into that list.

    >>> is_space = lambda c: c == " "
    >>> list(partitionby(is_space, "I have space"))
    [('I',), (' ',), ('h', 'a', 'v', 'e'), (' ',), ('s', 'p', 'a', 'c', 'e')]

    >>> is_large = lambda x: x > 10
    >>> list(partitionby(is_large, [1, 2, 1, 99, 88, 33, 99, -1, 5]))
    [(1, 2, 1), (99, 88, 33, 99), (-1, 5)]

    See also:
        partition
        groupby
        itertools.groupby
    """
    return map(tuple, pluck(1, itertools.groupby(seq, key=func)))


def collect(func):
    """ Decorate a generator and return a function, that returns a list instead.

    >>> @collect
    ... def odd_numbers(n):
    ...     for i in range(n):
    ...         yield 2 * i + 1
    >>> odd_numbers(3) # not a generator anymore
    [1, 3, 5]

    See also:
        composed
    """
    return composed(list)(func)
