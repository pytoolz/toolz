import random
import sys

# preserve random state
_randomstate = random.getstate()


# See #166: https://github.com/pytoolz/toolz/issues/166

class EqualityHashKey(object):
    """ Create a hash key that uses equality comparisons between items.

    This may be used to create hash keys for otherwise unhashable types:

    >>> set(map(EqualityHashKey, [[], [], [1], [1], {}]))  # doctest: +SKIP
    {=[]=, =[1]=, ={}=}

    **Caution:** adding N ``EqualityHashKey`` items to a hash container
    requires O(N**2) operations, not O(N) as for typical hashable types.
    Therefore, a suitable key function such as ``tuple`` or ``frozenset``
    is usually preferred if possible.

    ``EqualityHashKey`` *is* convenient to use, however, especially when
    a suitable key function is complicated or unavailable.  For example,
    the following returns all unique values based on equality:

    >>> from toolz import unique
    >>> vals = [[], [], [1], [1], [2], {}, {}, {}]
    >>> list(unique(vals, key=EqualityHashKey))
    [[], [1], [2], {}]

    The above example may be refined if many duplicate items are expected.
    This recipe efficiently filters out duplicate items based on id:

    >>> list(unique(unique(vals, key=id), key=EqualityHashKey))
    [[], [1], [2], {}]

    **Warning:** don't change the equality value of an item already in a hash
    containter.  Unhashable types are unhashable for a reason.  For example:

    >>> L1 = [1] ; L2 = [2]
    >>> s = set(map(EqualityHashKey, [L1, L2]))
    >>> print(s)  # doctest: +SKIP
    set([=[1]=, =[2]=])

    >>> L1[0] = 2  # Don't do this!  ``s`` now has duplicate items!
    >>> print(s)  # doctest: +SKIP
    set([=[2]=, =[2]=])

    Although this may appear problematic, immutable data types is a common
    idiom in functional programming, and``EqualityHashKey`` easily allows
    the same idiom to be used by convention rather than strict requirement.

    See Also:
        identity
    """
    __slots__ = 'item'
    _hashvalue = random.randint(-sys.maxsize-1, sys.maxsize)

    def __init__(self, item):
        self.item = item

    def __hash__(self):
        return self._hashvalue

    def __eq__(self, other):
        try:
            return (self._hashvalue == other._hashvalue and
                    self.item == other.item)
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return '=%s=' % str(self.item)

    def __repr__(self):
        return '=%s=' % repr(self.item)


# preserve random state
random.setstate(_randomstate)
