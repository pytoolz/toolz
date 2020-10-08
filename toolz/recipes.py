import itertools
from typing import TypeVar, Dict, Tuple, Callable, Any, Iterable, Sequence, \
    overload, List

from .itertoolz import frequencies, pluck, getter

__all__ = ('countby', 'partitionby')

A = TypeVar('A')
B = TypeVar('B')
KeyLike = TypeVar('KeyLike', int, Iterable, Callable, Tuple)


# Case: countby(len, ['cat', 'mouse', 'dog'])
@overload
def countby(key: Callable[[A], B], seq: Iterable[A]) -> Dict[B, int]: ...


# Case: countby('a', [{'a': 1, 'b': 2}, {'a': 10, 'b': 2}])
@overload
def countby(key: A, seq: Iterable[Dict[A, B]]) -> Dict[B, int]: ...


# Case: countby(0, [[1, 2], [10, 2]])
def countby(key: int, seq: Iterable[Iterable[A]]) -> Dict[A, int]: ...


# Case: countby([0, 1], [[1, 2], [10, 2]])
def countby(key: List[int],
            seq: Iterable[Iterable[A]]) -> Dict[Tuple[A, ...], int]: ...


def countby(key: KeyLike, seq: Iterable[Any]) -> Dict[Any, int]:
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
    return frequencies(map(key, seq))  # type: ignore


def partitionby(func: Callable[[A], bool],
                seq: Sequence[A]) -> Iterable[Tuple[A, ...]]:
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
