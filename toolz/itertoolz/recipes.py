from .core import groupby, frequencies
from toolz.compatibility import map


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
