from .core import groupby, identity


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
    return dict([(k, len(v)) for k, v in groupby(func, seq).items()])
