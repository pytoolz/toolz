from toolz import curry, unique, first
from toolz.sandbox.core import EqualityHashKey


def test_EqualityHashKey_default_key():
    # Is `EqualityHashDefault` a better name than `DefaultHashKey`?
    DefaultHashKey = curry(EqualityHashKey, None)
    L1 = [1]
    L2 = [2]
    data1 = [L1, L1, L2, [], [], [1], [2], {}, ()]
    set1 = set(map(DefaultHashKey, data1))
    set2 = set(map(DefaultHashKey, [[], [1], [2], {}, ()]))
    assert set1 == set2
    assert len(set1) == 5

    # Test that ``DefaultHashKey(item)`` is distinct from ``item``
    T0 = ()
    T1 = (1,)
    data2 = list(map(DefaultHashKey, [T0, T0, T1, T1, (), (1,)]))
    data2.extend([T0, T1, (), (1,)])
    set3 = set(data2)
    assert set3 == set([(), (1,), DefaultHashKey(()), DefaultHashKey((1,))])
    assert len(set3) == 4
    assert DefaultHashKey(()) in set3
    assert DefaultHashKey((1,)) in set3

    # Miscellaneous
    E1 = DefaultHashKey(L1)
    E2 = DefaultHashKey(L2)
    assert str(E1) == '=[1]='
    assert repr(E1) == '=[1]='
    assert E1 != E2
    assert not (E1 == E2)
    assert E1 == DefaultHashKey(L1)
    assert not (E1 != DefaultHashKey(L1))
    assert E1 != L1
    assert not (E1 == L1)


def test_EqualityHashKey_callable_key():
    # Common simple hash key functions.  Should these be renamed to
    # EqualityHashLen, EqualityHashType, EqualityHashId, and EqualityHashFirst?
    LenHashKey = curry(EqualityHashKey, len)
    TypeHashKey = curry(EqualityHashKey, type)
    IdHashKey = curry(EqualityHashKey, id)
    FirstHashKey = curry(EqualityHashKey, first)
    data1 = [[], [1], (), (1,), {}, {1: 2}]
    data2 = [[1, 2], (1, 2), (1, 3), [1, 3], [2, 1], {1: 2}]
    assert list(unique(data1*3, key=LenHashKey)) == data1
    assert list(unique(data2*3, key=LenHashKey)) == data2
    assert list(unique(data1*3, key=TypeHashKey)) == data1
    assert list(unique(data2*3, key=TypeHashKey)) == data2
    assert list(unique(data1*3, key=IdHashKey)) == data1
    assert list(unique(data2*3, key=IdHashKey)) == data2
    assert list(unique(data2*3, key=FirstHashKey)) == data2
