import itertools
import heapq
import collections
import operator
from functools import partial
from toolz.compatibility import map, filter, filterfalse, zip, zip_longest


__all__ = ('remove', 'accumulate', 'groupby', 'merge_sorted', 'interleave',
           'unique', 'isiterable', 'isdistinct', 'take', 'drop', 'take_nth',
           'first', 'second', 'nth', 'last', 'get', 'concat', 'concatv',
           'mapcat', 'cons', 'interpose', 'frequencies', 'reduceby', 'iterate',
           'sliding_window', 'partition', 'partition_all', 'count', 'pluck',
           'intersect_sorted')


identity = lambda x: x


def remove(predicate, seq):
    """ Return those items of sequence for which predicate(item) is False

    >>> def iseven(x):
    ...     return x % 2 == 0
    >>> list(remove(iseven, [1, 2, 3, 4]))
    [1, 3]
    """
    return filterfalse(predicate, seq)


def accumulate(binop, seq):
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

    See Also:
        itertools.accumulate :  In standard itertools for Python 3.2+
    """
    seq = iter(seq)
    result = next(seq)
    yield result
    for elem in seq:
        result = binop(result, elem)
        yield result


def groupby(func, seq):
    """ Group a collection by a key function

    >>> names = ['Alice', 'Bob', 'Charlie', 'Dan', 'Edith', 'Frank']
    >>> groupby(len, names)
    {3: ['Bob', 'Dan'], 5: ['Alice', 'Edith', 'Frank'], 7: ['Charlie']}

    >>> iseven = lambda x: x % 2 == 0
    >>> groupby(iseven, [1, 2, 3, 4, 5, 6, 7, 8])
    {False: [1, 3, 5, 7], True: [2, 4, 6, 8]}

    See Also:
        ``countby``
    """
    d = collections.defaultdict(list)
    for item in seq:
        d[func(item)].append(item)
    return dict(d)


def intersect_sorted(*seqs):
    """ Intersection of a collection of sorted iterables.

    Generates (once) each item that occurs in each of the iterables *seqs.

    >>> list(intersect_sorted([1, 1, 3, 5, 5], [1, 2, 3, 4, 5], [3, 4, 5]))
    [3, 5]
    """
    from itertools import groupby as itgroupby

    # Remove repeated elements from each iterable to make length check work.
    n = len(seqs)
    seqs = ((x for (x, _) in itgroupby(it)) for it in seqs)

    for x, group in itgroupby(merge_sorted(*seqs)):
        if sum(1 for _ in group) == n:
            yield x


def merge_sorted(*seqs, **kwargs):
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
    key = kwargs.get('key', None)
    if key is None:
        # heapq.merge does what we do below except by val instead of key(val)
        return heapq.merge(*seqs)
    else:
        return _merge_sorted_key(seqs, key)


def _merge_sorted_key(seqs, key):
    # The commented code below shows an alternative (slower) implementation
    # to apply a key function for sorting.
    #
    # mapper = lambda i, item: (key(item), i, item)
    # keyiters = [map(partial(mapper, i), itr) for i, itr in
    #             enumerate(seqs)]
    # return (item for (item_key, i, item) in heapq.merge(*keyiters))

    # binary heap as a priority queue
    pq = []

    # Initial population
    for itnum, it in enumerate(map(iter, seqs)):
        try:
            item = next(it)
            pq.append([key(item), itnum, item, it])
        except StopIteration:
            pass
    heapq.heapify(pq)

    # Repeatedly yield and then repopulate from the same iterator
    while True:
        try:
            while True:
                # raises IndexError when pq is empty
                _, itnum, item, it = s = pq[0]
                yield item
                item = next(it)  # raises StopIteration when exhausted
                s[0] = key(item)
                s[2] = item
                heapq.heapreplace(pq, s)  # restore heap condition
        except StopIteration:
            heapq.heappop(pq)  # remove empty iterator
        except IndexError:
            return


def interleave(seqs, pass_exceptions=()):
    """ Interleave a sequence of sequences

    >>> list(interleave([[1, 2], [3, 4]]))
    [1, 3, 2, 4]

    >>> ''.join(interleave(('ABC', 'XY')))
    'AXBYC'

    Both the individual sequences and the sequence of sequences may be infinite

    Returns a lazy iterator
    """
    iters = map(iter, seqs)
    while iters:
        newiters = []
        for itr in iters:
            try:
                yield next(itr)
                newiters.append(itr)
            except (StopIteration,) + tuple(pass_exceptions):
                pass
        iters = newiters


def unique(seq, key=identity):
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
    for item in seq:
        tag = key(item)
        if tag not in seen:
            seen.add(tag)
            yield item


def isiterable(x):
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


def isdistinct(seq):
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
    if iter(seq) is seq:
        seen = set()
        for item in seq:
            if item in seen:
                return False
            seen.add(item)
        return True
    else:
        return len(seq) == len(set(seq))


def take(n, seq):
    """ The first n elements of a sequence

    >>> list(take(2, [10, 20, 30, 40, 50]))
    [10, 20]
    """
    return itertools.islice(seq, n)


def drop(n, seq):
    """ The sequence following the first n elements

    >>> list(drop(2, [10, 20, 30, 40, 50]))
    [30, 40, 50]
    """
    return itertools.islice(seq, n, None)


def take_nth(n, seq):
    """ Every nth item in seq

    >>> list(take_nth(2, [10, 20, 30, 40, 50]))
    [10, 30, 50]
    """
    return itertools.islice(seq, 0, None, n)


def first(seq):
    """ The first element in a sequence

    >>> first('ABC')
    'A'
    """
    return next(iter(seq))


def second(seq):
    """ The second element in a sequence

    >>> second('ABC')
    'B'
    """
    return next(itertools.islice(seq, 1, None))


def nth(n, seq):
    """ The nth element in a sequence

    >>> nth(1, 'ABC')
    'B'
    """
    if isinstance(seq, (tuple, list, collections.Sequence)):
        return seq[n]
    else:
        return next(itertools.islice(seq, n, None))


def last(seq):
    """ The last element in a sequence

    >>> last('ABC')
    'C'
    """
    try:
        return seq[-1]
    except (TypeError, KeyError):
        return collections.deque(seq, 1)[0]


rest = partial(drop, 1)


no_default = '__no__default__'


def _get(ind, seq, default):
    try:
        return seq[ind]
    except (KeyError, IndexError):
        return default


def get(ind, seq, default=no_default):
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
        return seq[ind]
    except TypeError:  # `ind` may be a list
        if isinstance(ind, list):
            if default is no_default:
                return operator.itemgetter(*ind)(seq)
            else:
                return tuple(_get(i, seq, default) for i in ind)
        elif default is not no_default:
            return default
        else:
            raise
    except (KeyError, IndexError):  # we know `ind` is not a list
        if default is no_default:
            raise
        else:
            return default


def concat(seqs):
    """ Concatenate zero or more iterables, any of which may be infinite.

    An infinite sequence will prevent the rest of the arguments from
    being included.

    We use chain.from_iterable rather than chain(*seqs) so that seqs
    can be a generator.

    >>> list(concat([[], [1], [2, 3]]))
    [1, 2, 3]

    See also:
        itertools.chain.from_iterable  equivalent
    """
    return itertools.chain.from_iterable(seqs)


def concatv(*seqs):
    """ Variadic version of concat

    >>> list(concatv([], ["a"], ["b", "c"]))
    ['a', 'b', 'c']

    See also:
        itertools.chain
    """
    return concat(seqs)


def mapcat(func, seqs):
    """ Apply func to each sequence in seqs, concatenating results.

    >>> list(mapcat(lambda s: [c.upper() for c in s],
    ...             [["a", "b"], ["c", "d", "e"]]))
    ['A', 'B', 'C', 'D', 'E']
    """
    return concat(map(func, seqs))


def cons(el, seq):
    """ Add el to beginning of (possibly infinite) sequence seq.

    >>> list(cons(1, [2, 3]))
    [1, 2, 3]
    """
    yield el
    for s in seq:
        yield s


def interpose(el, seq):
    """ Introduce element between each pair of elements in seq

    >>> list(interpose("a", [1, 2, 3]))
    [1, 'a', 2, 'a', 3]
    """
    combined = zip(itertools.repeat(el), seq)
    return drop(1, concat(combined))


def frequencies(seq):
    """ Find number of occurrences of each value in seq

    >>> frequencies(['cat', 'cat', 'ox', 'pig', 'pig', 'cat'])  #doctest: +SKIP
    {'cat': 3, 'ox': 1, 'pig': 2}

    See Also:
        countby
        groupby
    """
    d = collections.defaultdict(int)
    for item in seq:
        d[item] += 1
    return dict(d)


def reduceby(key, binop, seq, init):
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

    >>> from operator import add, mul
    >>> data = [1, 2, 3, 4, 5]
    >>> iseven = lambda x: x % 2 == 0
    >>> reduceby(iseven, add, data, 0)
    {False: 9, True: 6}
    >>> reduceby(iseven, mul, data, 1)
    {False: 15, True: 8}

    >>> projects = [{'name': 'build roads', 'state': 'CA', 'cost': 1000000},
    ...             {'name': 'fight crime', 'state': 'IL', 'cost': 100000},
    ...             {'name': 'help farmers', 'state': 'IL', 'cost': 2000000},
    ...             {'name': 'help farmers', 'state': 'CA', 'cost': 200000}]
    >>> reduceby(lambda x: x['state'],              # doctest: +SKIP
    ...          lambda acc, x: acc + x['cost'],
    ...          projects, 0)
    {'CA': 1200000, 'IL': 2100000}
    """
    d = {}
    for item in seq:
        k = key(item)
        if k not in d:
            d[k] = init
        d[k] = binop(d[k], item)
    return d


def iterate(func, x):
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


def sliding_window(n, seq):
    """ A sequence of overlapping subsequences

    >>> list(sliding_window(2, [1, 2, 3, 4]))
    [(1, 2), (2, 3), (3, 4)]

    This function creates a sliding window suitable for transformations like
    sliding means / smoothing

    >>> mean = lambda seq: float(sum(seq)) / len(seq)
    >>> list(map(mean, sliding_window(2, [1, 2, 3, 4])))
    [1.5, 2.5, 3.5]
    """
    it = iter(seq)
    # An efficient FIFO data structure with maximum length
    d = collections.deque(itertools.islice(it, n), n)
    if len(d) != n:
        raise StopIteration()
    for item in it:
        yield tuple(d)
        d.append(item)
    yield tuple(d)


no_pad = '__no__pad__'


def partition(n, seq, pad=no_pad):
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
    else:
        return zip_longest(*args, fillvalue=pad)


def partition_all(n, seq):
    """ Partition all elements of sequence into tuples of length at most n

    The final tuple may be shorter to accommodate extra elements.

    >>> list(partition_all(2, [1, 2, 3, 4]))
    [(1, 2), (3, 4)]

    >>> list(partition_all(2, [1, 2, 3, 4, 5]))
    [(1, 2), (3, 4), (5,)]

    See Also:
        partition
    """
    args = [iter(seq)] * n
    it = zip_longest(*args, fillvalue=no_pad)
    prev = next(it)
    for item in it:
        yield prev
        prev = item
    if prev[-1] is no_pad:
        yield prev[:prev.index(no_pad)]
    else:
        yield prev


def count(seq):
    """ Count the number of items in seq

    Like the builtin ``len`` but works on lazy sequencies.

    Not to be confused with ``itertools.count``

    See also:
        len
    """
    if hasattr(seq, '__len__'):
        return len(seq)
    return sum(1 for i in seq)


def pluck(ind, seqs, default=no_default):
    """ plucks an element or several elements from each item in a sequence.

    ``pluck`` maps ``itertoolz.get`` over a sequence and returns one or more
    elements of each item in the sequence.

    This is equivalent to running `map(curried.get(ind), seqs)`

    ``ind`` can be either a single string/index or a sequence of
    strings/indices.
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
    if default is no_default:
        if isinstance(ind, list):
            return map(operator.itemgetter(*ind), seqs)
        return map(operator.itemgetter(ind), seqs)
    elif isinstance(ind, list):
        return (tuple(_get(item, seq, default) for item in ind)
                for seq in seqs)
    return (_get(ind, seq, default) for seq in seqs)
