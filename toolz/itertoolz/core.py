import itertools
from functools import partial
from toolz.compatibility import Queue, map


identity = lambda x: x


def remove(predicate, coll):
    """ Return those items of collection for which predicate(item) is true.

    >>> def even(x):
    ...     return x % 2 == 0
    >>> list(remove(even, [1, 2, 3, 4]))
    [1, 3]
    """
    return filter(lambda x: not predicate(x), coll)


def accumulate(f, seq):
    """ Repeatedly apply binary function f to a sequence, accumulating results

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
    result = next(iter(seq))
    yield result
    for elem in itertools.islice(seq, 1, None):
        result = f(result, elem)
        yield result


def groupby(f, coll):
    """ Group a collection by a key function

    >>> names = ['Alice', 'Bob', 'Charlie', 'Dan', 'Edith', 'Frank']
    >>> groupby(len, names)
    {3: ['Bob', 'Dan'], 5: ['Alice', 'Edith', 'Frank'], 7: ['Charlie']}
    """
    d = dict()
    for item in coll:
        key = f(item)
        if key not in d:
            d[key] = []
        d[key].append(item)
    return d


def merge_sorted(*iters, **kwargs):
    """ Merge and sort a collection of sorted collections

    >>> list(merge_sorted([1, 3, 5], [2, 4, 6]))
    [1, 2, 3, 4, 5, 6]

    >>> ''.join(merge_sorted('abc', 'abc', 'abc'))
    'aaabbbccc'
    """
    key = kwargs.get('key', identity)
    iters = map(iter, iters)
    pq = Queue.PriorityQueue()

    def inject_first_element(it, tiebreaker=None):
        try:
            item = next(it)
            pq.put((key(item), item, tiebreaker, it))
        except StopIteration:
            pass

    # Initial population
    for i, it in enumerate(iters):
        inject_first_element(it, i)

    # Repeatedly yield and then repopulate from the same iterator
    while not pq.empty():
        _, item, tb, it = pq.get()
        yield item
        inject_first_element(it, tb)


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


def intersection(*seqs):
    """ Lazily evaluated intersection of sequences

    >>> list(intersection([1, 2, 3], [2, 3, 4]))
    [2, 3]
    """
    return (item for item in seqs[0]
                 if all(item in seq for seq in seqs[1:]))


def iterable(x):
    """ Is x iterable?

    >>> iterable([1, 2, 3])
    True
    >>> iterable('abc')
    True
    >>> iterable(5)
    False
    """
    try:
        iter(x)
        return True
    except TypeError:
        return False


def distinct(seq):
    """ All values in sequence are distinct

    >>> distinct([1, 2, 3])
    True
    >>> distinct([1, 2, 1])
    False

    >>> distinct("Hello")
    False
    >>> distinct("World")
    True
    """
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


def first(seq):
    """ The first element in a sequence

    >>> first('ABC')
    'A'
    """
    return next(iter(seq))


def nth(n, seq):
    """ The nth element in a sequence

    >>> nth(1, 'ABC')
    'B'
    """
    try:
        return seq[n]
    except TypeError:
        return next(itertools.islice(seq, n, None))


def last(seq):
    """ The last element in a sequence

    >>> last('ABC')
    'C'
    """
    try:
        return seq[-1]
    except TypeError:
        old = None
        it = iter(seq)
        while True:
            try:
                old = next(it)
            except StopIteration:
                return old


second = partial(nth, 1)
rest = partial(drop, 1)


no_default = '__no__default__'


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
    """
    if isinstance(ind, list):
        return tuple(get(i, seq, default) for i in ind)
    if default is no_default:
        return seq[ind]
    else:
        try:
            return seq[ind]
        except (KeyError, IndexError):
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


def mapcat(f, seqs):
    """ Apply f to each sequence in seqs, concatenating results

    >>> list(mapcat(lambda s: [c.upper() for c in s],
    ...             [["a", "b"], ["c", "d", "e"]]))
    ['A', 'B', 'C', 'D', 'E']
    """
    return concat(map(f, seqs))


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
    return rest(mapcat(lambda x: [el, x], seq))


def frequencies(seq):
    """ Find number of occurrences of each value in seq

    >>> frequencies(['cat', 'cat', 'ox', 'pig', 'pig', 'cat'])  #doctest: +SKIP
    {'cat': 3, 'ox': 1, 'pig': 2}

    See Also:
        countby
        groupby
    """
    d = dict()
    for item in seq:
        try:
            d[item] += 1
        except KeyError:
            d[item] = 1
    return d


def reduceby(keyfn, binop, seq, init):
    """ Perform a simultaneous groupby and reduction

    The computation:
        result = reduceby(keyfn, binop, seq, init)

    is equivalent to the following:
        groups = groupby(keyfn, seq)

        def reduction(group):
            return reduce(binop, group, init)

        result = {k: reduction(group) for k, group in groups.items()}

    But the former does not build the intermediate groups, allowing it to
    operate in much less space.  This makes it suitable for larger datasets
    that do not fit comfortably in memory

    >>> from operator import add, mul
    >>> data = [1, 2, 3, 4, 5]
    >>> is_even = lambda x: x % 2 == 0
    >>> reduceby(is_even, add, data, 0)
    {False: 9, True: 6}
    >>> reduceby(is_even, mul, data, 1)
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
        key = keyfn(item)
        if key not in d:
            d[key] = init
        d[key] = binop(d[key], item)
    return d


def iterate(f, x):
    """ Repeatedly apply a function f onto an original input

    Yields x, then f(x), then f(f(x)), then f(f(f(x))), etc..

    >>> def inc(x):  return x + 1
    >>> it = iterate(inc, 0)
    >>> next(it)
    0
    >>> next(it)
    1
    >>> next(it)
    2
    """
    while True:
        yield x
        x = f(x)
