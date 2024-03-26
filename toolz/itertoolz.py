from __future__ import annotations

import collections
import heapq
import itertools
import operator
from collections.abc import (
    Callable,
    Generator,
    Iterator,
    Mapping,
    Sequence,
    Sized,
)
from functools import partial
from itertools import filterfalse, zip_longest
from random import Random
from typing import TYPE_CHECKING, Any, Iterable, TypeVar, cast, overload

from toolz.utils import no_default, no_pad

_T = TypeVar('_T')
_S = TypeVar('_S')
_U = TypeVar('_U')

if TYPE_CHECKING:
    from abc import abstractmethod
    from typing import Protocol

    from typing_extensions import TypeGuard  # >= py310

    from toolz.utils import NoDefaultType, NoPadType

    class Comparable(Protocol):
        """Protocol for annotating comparable types."""

        @abstractmethod
        def __lt__(self: _CT, other: _CT) -> bool:
            pass

    class Randomable(Protocol):
        def random(self) -> float: ...


    _CT = TypeVar('_CT', bound=Comparable)
    Predicate = Callable[[_T], object]
    BinaryOp = Callable[[_T, _T], _T]
    UnaryOp = Callable[[_T], _T]
    TransformOp = Callable[[_T], _S]
    SeqOrMapping = Sequence[_T] | Mapping[Any, _T]


__all__ = ('remove', 'accumulate', 'groupby', 'merge_sorted', 'interleave',
           'unique', 'isiterable', 'isdistinct', 'take', 'drop', 'take_nth',
           'first', 'second', 'nth', 'last', 'get', 'concat', 'concatv',
           'mapcat', 'cons', 'interpose', 'frequencies', 'reduceby', 'iterate',
           'sliding_window', 'partition', 'partition_all', 'count', 'pluck',
           'join', 'tail', 'diff', 'topk', 'peek', 'peekn', 'random_sample')


def _is_no_default(x: Any) -> TypeGuard[NoDefaultType]:
    if x is no_default:
        return True
    return False


def remove(predicate: Predicate[_T] | None, seq: Iterable[_T]) -> Iterator[_T]:
    """ Return those items of sequence for which predicate(item) is False

    >>> def iseven(x):
    ...     return x % 2 == 0
    >>> list(remove(iseven, [1, 2, 3, 4]))
    [1, 3]
    """
    return filterfalse(predicate, seq)


def accumulate(
    binop: BinaryOp[_T],
    seq: Iterable[_T],
    initial: _T | NoDefaultType = no_default,
) -> Generator[_T, None, None]:
    """ Repeatedly apply binary function to a sequence, accumulating results

    >>> from operator import add, mul
    >>> list(accumulate(add, [1, 2, 3, 4, 5]))
    [1, 3, 6, 10, 15]
    >>> list(accumulate(mul, [1, 2, 3, 4, 5]))
    [1, 2, 6, 24, 120]

    Accumulate is similar to ``reduce`` and is good for making functions like
    cumulative sum:

    >>> from functools import partial, reduce
    >>> sum    = partial(reduce, add)
    >>> cumsum = partial(accumulate, add)

    Accumulate also takes an optional argument that will be used as the first
    value. This is similar to reduce.

    >>> list(accumulate(add, [1, 2, 3], -1))
    [-1, 0, 2, 5]
    >>> list(accumulate(add, [], 1))
    [1]

    See Also:
        itertools.accumulate :  In standard itertools for Python 3.2+
    """
    seq = iter(seq)
    if _is_no_default(initial):
        try:
            result = next(seq)
        except StopIteration:
            return
    else:
        result = cast(_T, initial)
    yield result
    for elem in seq:
        result = binop(result, elem)
        yield result


# TODO: overload with key not callable
def groupby(key: TransformOp[_T, _S], seq: Iterable[_T]) -> dict[_S, list[_T]]:
    """ Group a collection by a key function

    >>> names = ['Alice', 'Bob', 'Charlie', 'Dan', 'Edith', 'Frank']
    >>> groupby(len, names)  # doctest: +SKIP
    {3: ['Bob', 'Dan'], 5: ['Alice', 'Edith', 'Frank'], 7: ['Charlie']}

    >>> iseven = lambda x: x % 2 == 0
    >>> groupby(iseven, [1, 2, 3, 4, 5, 6, 7, 8])  # doctest: +SKIP
    {False: [1, 3, 5, 7], True: [2, 4, 6, 8]}

    Non-callable keys imply grouping on a member.

    >>> groupby('gender', [{'name': 'Alice', 'gender': 'F'},
    ...                    {'name': 'Bob', 'gender': 'M'},
    ...                    {'name': 'Charlie', 'gender': 'M'}]) # doctest:+SKIP
    {'F': [{'gender': 'F', 'name': 'Alice'}],
     'M': [{'gender': 'M', 'name': 'Bob'},
           {'gender': 'M', 'name': 'Charlie'}]}

    Not to be confused with ``itertools.groupby``

    See Also:
        countby
    """
    if not callable(key):
        key = getter(key)
    d: dict[_S, list[_T]] = collections.defaultdict(list)
    for item in seq:
        vals = d[key(item)]
        vals.append(item)
    return d


def merge_sorted(
    *seqs: Iterable[_CT],
    key: UnaryOp[_CT] | None = None,
) -> Iterator[_CT]:
    """ Merge and sort a collection of sorted collections

    This works lazily and only keeps one value from each iterable in memory.

    >>> list(merge_sorted([1, 3, 5], [2, 4, 6]))
    [1, 2, 3, 4, 5, 6]

    >>> ''.join(merge_sorted('abc', 'abc', 'abc'))
    'aaabbbccc'

    The "key" function used to sort the input may be passed as a keyword.

    >>> list(merge_sorted([2, 3], [1, 3], key=lambda x: x // 3))
    [2, 1, 3, 3]
    """
    if len(seqs) == 0:
        return iter([])
    if len(seqs) == 1:
        return iter(seqs[0])

    if key is None:
        return _merge_sorted_binary(seqs)
    return _merge_sorted_binary_key(seqs, key)


def _merge_sorted_binary(seqs: Sequence[Iterable[_CT]]) -> Iterator[_CT]:
    mid = len(seqs) // 2
    L1 = seqs[:mid]
    seq1 = iter(L1[0]) if len(L1) == 1 else _merge_sorted_binary(L1)
    L2 = seqs[mid:]
    seq2 = iter(L2[0]) if len(L2) == 1 else _merge_sorted_binary(L2)

    try:
        val2 = next(seq2)
    except StopIteration:
        for val1 in seq1:
            yield val1
        return

    for val1 in seq1:
        if val2 < val1:
            yield val2
            for val2 in seq2:
                if val2 < val1:
                    yield val2
                else:
                    yield val1
                    break
            else:
                break
        else:
            yield val1
    else:
        yield val2
        for val2 in seq2:
            yield val2
        return
    yield val1
    for val1 in seq1:
        yield val1


def _merge_sorted_binary_key(
    seqs: Sequence[Iterable[_CT]],
    key: UnaryOp[_CT],
) -> Iterator[_CT]:
    mid = len(seqs) // 2
    L1 = seqs[:mid]
    seq1 = iter(L1[0]) if len(L1) == 1 else _merge_sorted_binary_key(L1, key)
    L2 = seqs[mid:]
    seq2 = iter(L2[0]) if len(L2) == 1 else _merge_sorted_binary_key(L2, key)

    try:
        val2 = next(seq2)
    except StopIteration:
        for val1 in seq1:
            yield val1
        return
    key2 = key(val2)

    for val1 in seq1:
        key1 = key(val1)
        if key2 < key1:
            yield val2
            for val2 in seq2:
                key2 = key(val2)
                if key2 < key1:
                    yield val2
                else:
                    yield val1
                    break
            else:
                break
        else:
            yield val1
    else:
        yield val2
        for val2 in seq2:
            yield val2
        return
    yield val1
    for val1 in seq1:
        yield val1


def interleave(seqs: Sequence[Sequence[_T]]) -> Iterator[_T]:
    """ Interleave a sequence of sequences

    >>> list(interleave([[1, 2], [3, 4]]))
    [1, 3, 2, 4]

    >>> ''.join(interleave(('ABC', 'XY')))
    'AXBYC'

    Both the individual sequences and the sequence of sequences may be infinite

    Returns a lazy iterator
    """
    iters: Iterator[Iterator[_T]] = itertools.cycle(map(iter, seqs))
    while True:
        try:
            for itr in iters:
                yield next(itr)
            return
        except StopIteration:
            predicate = partial(operator.is_not, itr)
            iters = itertools.cycle(itertools.takewhile(predicate, iters))


def unique(
    seq: Sequence[_T],
    key: TransformOp[_T, Any] | None = None,
) -> Iterator[_T]:
    """ Return only unique elements of a sequence

    >>> tuple(unique((1, 2, 3)))
    (1, 2, 3)
    >>> tuple(unique((1, 2, 1, 3)))
    (1, 2, 3)

    Uniqueness can be defined by key keyword

    >>> tuple(unique(['cat', 'mouse', 'dog', 'hen'], key=len))
    ('cat', 'mouse')
    """
    seen = set()
    if key is None:
        for item in seq:
            if item not in seen:
                seen.add(item)
                yield item
    else:  # calculate key
        for item in seq:
            val = key(item)
            if val not in seen:
                seen.add(val)
                yield item


def isiterable(x: Any) -> TypeGuard[Iterable]:
    """ Is x iterable?

    >>> isiterable([1, 2, 3])
    True
    >>> isiterable('abc')
    True
    >>> isiterable(5)
    False
    """
    try:
        iter(x)
        return True
    except TypeError:
        return False


def isdistinct(seq: Iterable | Sequence) -> bool:
    """ All values in sequence are distinct

    >>> isdistinct([1, 2, 3])
    True
    >>> isdistinct([1, 2, 1])
    False

    >>> isdistinct("Hello")
    False
    >>> isdistinct("World")
    True
    """
    if isinstance(seq, Sequence):
        return len(seq) == len(set(seq))

    seen = set()
    for item in seq:
        if item in seen:
            return False
        seen.add(item)
    return True


def take(n: int, seq: Iterable[_T]) -> Iterator[_T]:
    """ The first n elements of a sequence

    >>> list(take(2, [10, 20, 30, 40, 50]))
    [10, 20]

    See Also:
        drop
        tail
    """
    return itertools.islice(seq, n)


def tail(n: int, seq: Sequence[_T]) -> Sequence[_T]:
    """ The last n elements of a sequence

    >>> tail(2, [10, 20, 30, 40, 50])
    [40, 50]

    See Also:
        drop
        take
    """
    try:
        return seq[-n:]
    except (TypeError, KeyError):
        return tuple(collections.deque(seq, n))


def drop(n: int, seq: Sequence[_T]) -> Iterator[_T]:
    """ The sequence following the first n elements

    >>> list(drop(2, [10, 20, 30, 40, 50]))
    [30, 40, 50]

    See Also:
        take
        tail
    """
    return itertools.islice(seq, n, None)


def take_nth(n: int, seq: Sequence[_T]) -> Iterator[_T]:
    """ Every nth item in seq

    >>> list(take_nth(2, [10, 20, 30, 40, 50]))
    [10, 30, 50]
    """
    return itertools.islice(seq, 0, None, n)


def first(seq: Iterable[_T]) -> _T:
    """ The first element in a sequence

    >>> first('ABC')
    'A'
    """
    return next(iter(seq))


def second(seq: Iterable[_T]) -> _T:
    """ The second element in a sequence

    >>> second('ABC')
    'B'
    """
    seq = iter(seq)
    next(seq)
    return next(seq)


def nth(n: int, seq: Iterable[_T] | Sequence[_T]) -> _T:
    """ The nth element in a sequence

    >>> nth(1, 'ABC')
    'B'
    """
    if isinstance(seq, Sequence):
        return seq[n]
    return next(itertools.islice(seq, n, None))


def last(seq: Sequence[_T]) -> _T:
    """ The last element in a sequence

    >>> last('ABC')
    'C'
    """
    return tail(1, seq)[0]


rest = partial(drop, 1)


def _get(ind: Any, seq: SeqOrMapping[_T], default: _T) -> _T:
    try:
        return seq[ind]
    except (KeyError, IndexError):
        return default


@overload
def get(  # type: ignore[overload-overlap]
    ind: Sequence[Any],
    seq: SeqOrMapping[_T],
    default: _T | NoDefaultType = ...,
) -> tuple[_T, ...]: ...

@overload
def get(
    ind: Any,
    seq: SeqOrMapping[_T],
    default: _T | NoDefaultType = ...,
) -> _T: ...

def get(
    ind: Any | Sequence[Any],
    seq: SeqOrMapping[_T],
    default: _T | NoDefaultType = no_default,
) -> _T | tuple[_T, ...]:
    """ Get element in a sequence or dict

    Provides standard indexing

    >>> get(1, 'ABC')       # Same as 'ABC'[1]
    'B'

    Pass a list to get multiple values

    >>> get([1, 2], 'ABC')  # ('ABC'[1], 'ABC'[2])
    ('B', 'C')

    Works on any value that supports indexing/getitem
    For example here we see that it works with dictionaries

    >>> phonebook = {'Alice':  '555-1234',
    ...              'Bob':    '555-5678',
    ...              'Charlie':'555-9999'}
    >>> get('Alice', phonebook)
    '555-1234'

    >>> get(['Alice', 'Bob'], phonebook)
    ('555-1234', '555-5678')

    Provide a default for missing values

    >>> get(['Alice', 'Dennis'], phonebook, None)
    ('555-1234', None)

    See Also:
        pluck
    """
    try:
        return seq[ind]  # type: ignore[index]
    except TypeError:  # `ind` may be a list
        if isinstance(ind, list):
            if _is_no_default(default):
                if len(ind) > 1:
                    return tuple(operator.itemgetter(*ind)(seq))
                if ind:
                    return (seq[ind[0]],)
                return ()
            return tuple(_get(i, seq, cast(_T, default)) for i in ind)

        if not _is_no_default(default):
            return cast(_T, default)
        raise
    except (KeyError, IndexError):  # we know `ind` is not a list
        if not _is_no_default(default):
            return cast(_T, default)
        raise


def concat(seqs: Iterable[Iterable[_T]]) -> Iterator[_T]:
    """ Concatenate zero or more iterables, any of which may be infinite.

    An infinite sequence will prevent the rest of the arguments from
    being included.

    We use chain.from_iterable rather than ``chain(*seqs)`` so that seqs
    can be a generator.

    >>> list(concat([[], [1], [2, 3]]))
    [1, 2, 3]

    See also:
        itertools.chain.from_iterable  equivalent
    """
    return itertools.chain.from_iterable(seqs)


def concatv(*seqs: Iterable[_T]) -> Iterator[_T]:
    """ Variadic version of concat

    >>> list(concatv([], ["a"], ["b", "c"]))
    ['a', 'b', 'c']

    See also:
        itertools.chain
    """
    return concat(seqs)


def mapcat(
    func: TransformOp[Iterable[_T], Iterable[_S]],
    seqs: Iterable[Iterable[_T]],
) -> Iterator[_S]:
    """ Apply func to each sequence in seqs, concatenating results.

    >>> list(mapcat(lambda s: [c.upper() for c in s],
    ...             [["a", "b"], ["c", "d", "e"]]))
    ['A', 'B', 'C', 'D', 'E']
    """
    return concat(map(func, seqs))


def cons(el: _T, seq: Iterable[_T]) -> Iterator[_T]:
    """ Add el to beginning of (possibly infinite) sequence seq.

    >>> list(cons(1, [2, 3]))
    [1, 2, 3]
    """
    return itertools.chain([el], seq)


def interpose(el: _T, seq: Iterable[_T]) -> Iterator[_T]:
    """ Introduce element between each pair of elements in seq

    >>> list(interpose("a", [1, 2, 3]))
    [1, 'a', 2, 'a', 3]
    """
    inposed = concat(zip(itertools.repeat(el), seq))
    next(inposed)
    return inposed


def frequencies(seq: Iterable[_T]) -> dict[_T, int]:
    """ Find number of occurrences of each value in seq

    >>> frequencies(['cat', 'cat', 'ox', 'pig', 'pig', 'cat'])  #doctest: +SKIP
    {'cat': 3, 'ox': 1, 'pig': 2}

    See Also:
        countby
        groupby
    """
    d: dict[_T, int] = collections.defaultdict(int)
    for item in seq:
        d[item] += 1
    return d


# TODO: overload with key not callable
def reduceby(
    key: TransformOp[_T, _S],
    binop: BinaryOp[_T],
    seq: Iterable[_T],
    init: _T | Callable[[], _T] | NoDefaultType = no_default,
) -> dict[_S, _T]:
    """ Perform a simultaneous groupby and reduction

    The computation:

    >>> result = reduceby(key, binop, seq, init)      # doctest: +SKIP

    is equivalent to the following:

    >>> def reduction(group):                           # doctest: +SKIP
    ...     return reduce(binop, group, init)           # doctest: +SKIP

    >>> groups = groupby(key, seq)                    # doctest: +SKIP
    >>> result = valmap(reduction, groups)              # doctest: +SKIP

    But the former does not build the intermediate groups, allowing it to
    operate in much less space.  This makes it suitable for larger datasets
    that do not fit comfortably in memory

    The ``init`` keyword argument is the default initialization of the
    reduction.  This can be either a constant value like ``0`` or a callable
    like ``lambda : 0`` as might be used in ``defaultdict``.

    Simple Examples
    ---------------

    >>> from operator import add, mul
    >>> iseven = lambda x: x % 2 == 0

    >>> data = [1, 2, 3, 4, 5]

    >>> reduceby(iseven, add, data)  # doctest: +SKIP
    {False: 9, True: 6}

    >>> reduceby(iseven, mul, data)  # doctest: +SKIP
    {False: 15, True: 8}

    Complex Example
    ---------------

    >>> projects = [{'name': 'build roads', 'state': 'CA', 'cost': 1000000},
    ...             {'name': 'fight crime', 'state': 'IL', 'cost': 100000},
    ...             {'name': 'help farmers', 'state': 'IL', 'cost': 2000000},
    ...             {'name': 'help farmers', 'state': 'CA', 'cost': 200000}]

    >>> reduceby('state',                        # doctest: +SKIP
    ...          lambda acc, x: acc + x['cost'],
    ...          projects, 0)
    {'CA': 1200000, 'IL': 2100000}

    Example Using ``init``
    ----------------------

    >>> def set_add(s, i):
    ...     s.add(i)
    ...     return s

    >>> reduceby(iseven, set_add, [1, 2, 3, 4, 1, 2, 3], set)  # doctest: +SKIP
    {True:  set([2, 4]),
     False: set([1, 3])}
    """
    if not callable(key):
        key = getter(key)

    d = {}
    for item in seq:
        k = key(item)
        if k not in d:
            if _is_no_default(init):
                d[k] = item
                continue
            if callable(init):
                d[k] = init()
            else:
                d[k] = cast(_T, init)
        d[k] = binop(d[k], item)
    return d


def iterate(func: UnaryOp[_T], x: _T) -> Iterator[_T]:
    """ Repeatedly apply a function func onto an original input

    Yields x, then func(x), then func(func(x)), then func(func(func(x))), etc..

    >>> def inc(x):  return x + 1
    >>> counter = iterate(inc, 0)
    >>> next(counter)
    0
    >>> next(counter)
    1
    >>> next(counter)
    2

    >>> double = lambda x: x * 2
    >>> powers_of_two = iterate(double, 1)
    >>> next(powers_of_two)
    1
    >>> next(powers_of_two)
    2
    >>> next(powers_of_two)
    4
    >>> next(powers_of_two)
    8
    """
    while True:
        yield x
        x = func(x)


def sliding_window(n: int, seq: Iterable[_T]) -> Iterator[tuple[_T, ...]]:
    """ A sequence of overlapping subsequences

    >>> list(sliding_window(2, [1, 2, 3, 4]))
    [(1, 2), (2, 3), (3, 4)]

    This function creates a sliding window suitable for transformations like
    sliding means / smoothing

    >>> mean = lambda seq: float(sum(seq)) / len(seq)
    >>> list(map(mean, sliding_window(2, [1, 2, 3, 4])))
    [1.5, 2.5, 3.5]
    """
    return zip(
        *(
            collections.deque(itertools.islice(it, i), 0) or it
            for i, it in enumerate(itertools.tee(seq, n))
        )
    )


def partition(
    n: int,
    seq: Iterable[_T],
    pad: _S | NoPadType = no_pad,
) -> Iterator[tuple[_T | _S, ...]]:
    """ Partition sequence into tuples of length n

    >>> list(partition(2, [1, 2, 3, 4]))
    [(1, 2), (3, 4)]

    If the length of ``seq`` is not evenly divisible by ``n``, the final tuple
    is dropped if ``pad`` is not specified, or filled to length ``n`` by pad:

    >>> list(partition(2, [1, 2, 3, 4, 5]))
    [(1, 2), (3, 4)]

    >>> list(partition(2, [1, 2, 3, 4, 5], pad=None))
    [(1, 2), (3, 4), (5, None)]

    See Also:
        partition_all
    """
    args = [iter(seq)] * n
    if pad is no_pad:
        return zip(*args)
    return zip_longest(*args, fillvalue=pad)


def partition_all(n: int, seq: Sequence[_T]) -> Iterator[tuple[_T, ...]]:
    """ Partition all elements of sequence into tuples of length at most n

    The final tuple may be shorter to accommodate extra elements.

    >>> list(partition_all(2, [1, 2, 3, 4]))
    [(1, 2), (3, 4)]

    >>> list(partition_all(2, [1, 2, 3, 4, 5]))
    [(1, 2), (3, 4), (5,)]

    See Also:
        partition
    """

    def cast_out(val: tuple) -> tuple[_T, ...]:
        # Trick for type-checkers, `prev` type can contain `no_pad`
        # so cast to a type without `no_pad`
        return cast('tuple[_T, ...]', val)

    args = [iter(seq)] * n
    it = zip_longest(*args, fillvalue=no_pad)
    try:
        prev = next(it)
    except StopIteration:
        return
    for item in it:
        yield cast_out(prev)
        prev = item
    if prev[-1] is no_pad:
        try:
            # If seq defines __len__, then
            # we can quickly calculate where no_pad starts
            yield cast_out(prev[: len(seq) % n])
        except TypeError:
            # Get first index of no_pad without using .index()
            # https://github.com/pytoolz/toolz/issues/387
            # Binary search from CPython's bisect module,
            # modified for identity testing.
            lo, hi = 0, n
            while lo < hi:
                mid = (lo + hi) // 2
                if prev[mid] is no_pad:
                    hi = mid
                else:
                    lo = mid + 1
            yield cast_out(prev[:lo])
    else:
        yield cast_out(prev)


def count(seq: Iterable) -> int:
    """ Count the number of items in seq

    Like the builtin ``len`` but works on lazy sequences.

    Not to be confused with ``itertools.count``

    See also:
        len
    """
    if isinstance(seq, Sized):
        return len(seq)
    return sum(1 for _ in seq)


@overload
def pluck(  # type: ignore[overload-overlap]
    index: Sequence[Any],
    seqs: Iterable[SeqOrMapping[_T]],
    default: _T | NoDefaultType = ...,
) -> Iterator[tuple[_T, ...]]: ...


@overload
def pluck(
    index: Any,
    seqs: Iterable[SeqOrMapping[_T]],
    default: _T | NoDefaultType = ...,
) -> Iterator[_T]: ...


def pluck(  # type: ignore[misc]
    ind: Any | Sequence[Any],
    seqs: Iterable[SeqOrMapping[_T]],
    default: _T | NoDefaultType = no_default,
) -> Iterator[_T] | Iterator[tuple[_T, ...]]:
    """ plucks an element or several elements from each item in a sequence.

    ``pluck`` maps ``itertoolz.get`` over a sequence and returns one or more
    elements of each item in the sequence.

    This is equivalent to running `map(curried.get(ind), seqs)`

    ``ind`` can be either a single string/index or a list of strings/indices.
    ``seqs`` should be sequence containing sequences or dicts.

    e.g.

    >>> data = [{'id': 1, 'name': 'Cheese'}, {'id': 2, 'name': 'Pies'}]
    >>> list(pluck('name', data))
    ['Cheese', 'Pies']
    >>> list(pluck([0, 1], [[1, 2, 3], [4, 5, 7]]))
    [(1, 2), (4, 5)]

    See Also:
        get
        map
    """
    if _is_no_default(default):
        get = getter(ind)
        return map(get, seqs)

    if isinstance(ind, list):
        return (
            tuple(_get(item, seq, cast(_T, default)) for item in ind)
            for seq in seqs
        )
    return (_get(ind, seq, cast(_T, default)) for seq in seqs)


@overload
def getter(  # type: ignore[overload-overlap]
    index: list[Any],
) -> Callable[[SeqOrMapping[_T]], tuple[_T, ...]]: ...


@overload
def getter(index: Any) -> Callable[[Sequence[_T] | Mapping[Any, _T]], _T]: ...


def getter(
    index: Any | list[Any],
) -> Callable[[SeqOrMapping[_T]], _T | tuple[_T, ...]]:
    if isinstance(index, list):
        if len(index) == 1:
            index = index[0]
            return lambda x: (x[index],)
        if index:
            return operator.itemgetter(*index)
        return lambda _: ()
    return operator.itemgetter(index)


# TODO: overload with leftkey/rightkey not callable
def join(
    leftkey: TransformOp[_T, Any],
    leftseq: Iterable[_T],
    rightkey: TransformOp[_T, Any],
    rightseq: Iterable[_T],
    left_default: _U | NoDefaultType = no_default,
    right_default: _U | NoDefaultType = no_default,
) -> Iterator[tuple[_T | _U, _T | _U]]:
    """Join two sequences on common attributes

    This is a semi-streaming operation.  The LEFT sequence is fully evaluated
    and placed into memory.  The RIGHT sequence is evaluated lazily and so can
    be arbitrarily large.
    (Note: If right_default is defined, then unique keys of rightseq
        will also be stored in memory.)

    >>> friends = [('Alice', 'Edith'),
    ...            ('Alice', 'Zhao'),
    ...            ('Edith', 'Alice'),
    ...            ('Zhao', 'Alice'),
    ...            ('Zhao', 'Edith')]

    >>> cities = [('Alice', 'NYC'),
    ...           ('Alice', 'Chicago'),
    ...           ('Dan', 'Sydney'),
    ...           ('Edith', 'Paris'),
    ...           ('Edith', 'Berlin'),
    ...           ('Zhao', 'Shanghai')]

    >>> # Vacation opportunities
    >>> # In what cities do people have friends?
    >>> result = join(second, friends,
    ...               first, cities)
    >>> for ((a, b), (c, d)) in sorted(unique(result)):
    ...     print((a, d))
    ('Alice', 'Berlin')
    ('Alice', 'Paris')
    ('Alice', 'Shanghai')
    ('Edith', 'Chicago')
    ('Edith', 'NYC')
    ('Zhao', 'Chicago')
    ('Zhao', 'NYC')
    ('Zhao', 'Berlin')
    ('Zhao', 'Paris')

    Specify outer joins with keyword arguments ``left_default`` and/or
    ``right_default``.  Here is a full outer join in which unmatched elements
    are paired with None.

    >>> identity = lambda x: x
    >>> list(join(identity, [1, 2, 3],
    ...           identity, [2, 3, 4],
    ...           left_default=None, right_default=None))
    [(2, 2), (3, 3), (None, 4), (1, None)]

    Usually the key arguments are callables to be applied to the sequences.  If
    the keys are not obviously callable then it is assumed that indexing was
    intended, e.g. the following is a legal change.
    The join is implemented as a hash join and the keys of leftseq must be
    hashable. Additionally, if right_default is defined, then keys of rightseq
    must also be hashable.

    >>> # result = join(second, friends, first, cities)
    >>> result = join(1, friends, 0, cities)  # doctest: +SKIP
    """
    if not callable(leftkey):
        leftkey = getter(leftkey)
    if not callable(rightkey):
        rightkey = getter(rightkey)

    d = groupby(leftkey, leftseq)

    if _is_no_default(left_default) and _is_no_default(right_default):
        # Inner Join
        for item in rightseq:
            key = rightkey(item)
            if key in d:
                for left_match in d[key]:
                    ret = (left_match, item)
                    yield cast("tuple[_T | _U, _T | _U]", ret)
    elif not _is_no_default(left_default) and _is_no_default(right_default):
        # Right Join
        for item in rightseq:
            key = rightkey(item)
            if key in d:
                for left_match in d[key]:
                    yield (left_match, item)
            else:
                yield (cast(_U, left_default), item)
    elif not _is_no_default(right_default):
        seen_keys = set()

        if _is_no_default(left_default):
            # Left Join
            for item in rightseq:
                key = rightkey(item)
                seen_keys.add(key)
                if key in d:
                    for left_match in d[key]:
                        yield (left_match, item)
        else:
            # Full Join
            for item in rightseq:
                key = rightkey(item)
                seen_keys.add(key)
                if key in d:
                    for left_match in d[key]:
                        yield (left_match, item)
                else:
                    yield (cast(_U, left_default), item)

        for key, matches in d.items():
            if key not in seen_keys:
                for match in matches:
                    yield (match, cast(_U, right_default))


def diff(
    *seqs: Iterable[_T],
    default: _T | NoDefaultType = no_default,
    key: TransformOp[_T, Any] | None = None,
) -> Iterator[tuple[_T, ...]]:
    """ Return those items that differ between sequences

    >>> list(diff([1, 2, 3], [1, 2, 10, 100]))
    [(3, 10)]

    Shorter sequences may be padded with a ``default`` value:

    >>> list(diff([1, 2, 3], [1, 2, 10, 100], default=None))
    [(3, 10), (None, 100)]

    A ``key`` function may also be applied to each item to use during
    comparisons:

    >>> list(diff(['apples', 'bananas'], ['Apples', 'Oranges'], key=str.lower))
    [('bananas', 'Oranges')]
    """
    N = len(seqs)
    if N == 1 and isinstance(seqs[0], list):
        all_seqs: Iterable[Iterable[_T]] = seqs[0]
        N = len(list(all_seqs))
    else:
        all_seqs = cast(Iterable[Iterable[_T]], seqs)
    if N < 2:
        raise TypeError('Too few sequences given (min 2 required)')

    if not _is_no_default(default):
        iters = cast(
            "Iterator[tuple[_T, ...]]",
            zip_longest(*all_seqs, fillvalue=default),
        )
    else:
        iters = zip(*all_seqs)
    if key is None:
        for items in iters:
            if items.count(items[0]) != N:
                yield items
    else:
        for items in iters:
            vals = tuple(map(key, items))
            if vals.count(vals[0]) != N:
                yield items


def topk(
    k: int,
    seq: Iterable[_T],
    key: Predicate[_T] | Any | None = None,
) -> tuple[_T, ...]:
    """ Find the k largest elements of a sequence

    Operates lazily in ``n*log(k)`` time

    >>> topk(2, [1, 100, 10, 1000])
    (1000, 100)

    Use a key function to change sorted order

    >>> topk(2, ['Alice', 'Bob', 'Charlie', 'Dan'], key=len)
    ('Charlie', 'Alice')

    See also:
        heapq.nlargest
    """
    if key is not None and not callable(key):
        key = getter(key)
    return tuple(heapq.nlargest(k, seq, key=key))


def peek(seq: Iterable[_T]) -> tuple[_T, Iterator[_T]]:
    """ Retrieve the next element of a sequence

    Returns the first element and an iterable equivalent to the original
    sequence, still having the element retrieved.

    >>> seq = [0, 1, 2, 3, 4]
    >>> first, seq = peek(seq)
    >>> first
    0
    >>> list(seq)
    [0, 1, 2, 3, 4]
    """
    iterator = iter(seq)
    item = next(iterator)
    return item, itertools.chain((item,), iterator)


def peekn(n: int, seq: Iterable[_T]) -> tuple[tuple[_T, ...], Iterator[_T]]:
    """ Retrieve the next n elements of a sequence

    Returns a tuple of the first n elements and an iterable equivalent
    to the original, still having the elements retrieved.

    >>> seq = [0, 1, 2, 3, 4]
    >>> first_two, seq = peekn(2, seq)
    >>> first_two
    (0, 1)
    >>> list(seq)
    [0, 1, 2, 3, 4]
    """
    iterator = iter(seq)
    peeked = tuple(take(n, iterator))
    return peeked, itertools.chain(iter(peeked), iterator)


def _has_random(random_state: Any) -> TypeGuard[Randomable]:
    if hasattr(random_state, 'random'):
        return True
    return False


def random_sample(
    prob: float,
    seq: Iterable[_T],
    random_state: int | Randomable | None = None,
) -> Iterator[_T]:
    """ Return elements from a sequence with probability of prob

    Returns a lazy iterator of random items from seq.

    ``random_sample`` considers each item independently and without
    replacement. See below how the first time it returned 13 items and the
    next time it returned 6 items.

    >>> seq = list(range(100))
    >>> list(random_sample(0.1, seq)) # doctest: +SKIP
    [6, 9, 19, 35, 45, 50, 58, 62, 68, 72, 78, 86, 95]
    >>> list(random_sample(0.1, seq)) # doctest: +SKIP
    [6, 44, 54, 61, 69, 94]

    Providing an integer seed for ``random_state`` will result in
    deterministic sampling. Given the same seed it will return the same sample
    every time.

    >>> list(random_sample(0.1, seq, random_state=2016))
    [7, 9, 19, 25, 30, 32, 34, 48, 59, 60, 81, 98]
    >>> list(random_sample(0.1, seq, random_state=2016))
    [7, 9, 19, 25, 30, 32, 34, 48, 59, 60, 81, 98]

    ``random_state`` can also be any object with a method ``random`` that
    returns floats between 0.0 and 1.0 (exclusive).

    >>> from random import Random
    >>> randobj = Random(2016)
    >>> list(random_sample(0.1, seq, random_state=randobj))
    [7, 9, 19, 25, 30, 32, 34, 48, 59, 60, 81, 98]
    """
    if not _has_random(random_state):
        random_state = Random(random_state)  # noqa: S311
    return filter(lambda _: random_state.random() < prob, seq)
