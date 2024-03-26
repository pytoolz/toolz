from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, Any

from .itertoolz import frequencies, getter, pluck

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator
    from typing import TypeVar

    from .itertoolz import TransformOp

    _T = TypeVar('_T')


__all__ = ('countby', 'partitionby')


def countby(key: Any, seq: Iterable[_T]) -> dict[_T, int]:
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


def partitionby(
    func: TransformOp[_T, Any], seq: Iterable[_T]
) -> Iterator[tuple[_T, ...]]:
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
