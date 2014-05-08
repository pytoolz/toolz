

# See #166: https://github.com/pytoolz/toolz/issues/166
# See #173: https://github.com/pytoolz/toolz/pull/173
#
# Qustions:
#   - What should be allowable as a `key`?
#       - **CURRENT**: all of the below
#       - A callable that calculates a key to hash given `item`
#           - Should the default key be used if the callable returns `None`?
#               - **CURRENT**: raise TypeError in `__hash__`
#           - What if the callable returns an unhashable object?
#               - **CURRENT**: raise TypeError in `__hash__`
#       - An object to use as a key to hash
#           - What if the object is unhashable?
#               - **CURRENT**: raise TypeError (if not None) in `__hash__`
#       - `None` to specify the default key should be used
#
#   - Should `key` be a positional or keyword argument?
#       - **CURRENT**: positional argument
#       - Erik: I like positional for many reasons:
#           - Easiest to use with curry
#           - Using the inefficient default key must be explicit, which is
#             much better than using it by default if `key` isn't provided
#           - I don't like keyword arguments :)
#
#   - Should the hash value be calculated in `__hash__` or `__init__`?
#       - **CURRENT**: in `__hash__`
#       - `__hash__`:
#           - this is overall cleaner
#           - expected behavior (probably)
#           - `key` attribute is understandable and usable
#       - `__init__`:
#           - precalculated hash for faster performance of repeated hashing
#           - hash value may be used in `__eq__` instead of `_default_hashkey`
#           - find out during object creation if the provided key is unhashable
#
#   - Should `DefaultHashKey` in the docstring be renamed to
#     `EqualityHashDefault`?
#       - This can perhaps lead to clearer naming conventions such as:
#           - EqualityHashLen, EqualityHashType, EqualityHashId, and
#             EqualityHashFirst
#
# Todo:
#   - Document `key` argument
#       - We can probably remove the refined `unique(unique(...))` recipe
#   - Test various uses of `key` argument
#   - Test other behaviors as they are finalized
#   - Add technical discussion as code comments describing how and why
#     this works
#
class EqualityHashKey(object):
    """ Create a hash key that uses equality comparisons between items.

    This may be used to create hash keys for otherwise unhashable types:

    >>> from toolz import curry
    >>> DefaultHashKey = curry(EqualityHashKey, None)
    >>> set(map(DefaultHashKey, [[], [], [1], [1], {}]))  # doctest: +SKIP
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
    >>> list(unique(vals, key=DefaultHashKey))
    [[], [1], [2], {}]

    The above example may be refined if many duplicate items are expected.
    This recipe efficiently filters out duplicate items based on id:

    >>> list(unique(unique(vals, key=id), key=DefaultHashKey))
    [[], [1], [2], {}]

    **Warning:** don't change the equality value of an item already in a hash
    containter.  Unhashable types are unhashable for a reason.  For example:

    >>> L1 = [1] ; L2 = [2]
    >>> s = set(map(DefaultHashKey, [L1, L2]))
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
    __slots__ = ['item', 'key']
    _default_hashkey = '__default__hashkey__'

    def __init__(self, key, item):
        if key is None:
            self.key = self._default_hashkey
        else:
            self.key = key
        self.item = item

    def __hash__(self):
        if callable(self.key):
            val = self.key(self.item)
            return hash(val)
        return hash(self.key)

    def __eq__(self, other):
        try:
            return (self._default_hashkey == other._default_hashkey and
                    self.item == other.item)
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return '=%s=' % str(self.item)

    def __repr__(self):
        return '=%s=' % repr(self.item)
