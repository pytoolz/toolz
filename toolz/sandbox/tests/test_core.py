from toolz.sandbox.core import EqualityHashKey


def test_EqualityHashKey():
    L1 = [1]
    L2 = [2]
    data1 = [L1, L1, L2, [], [], [1], [2], {}, ()]
    set1 = set(map(EqualityHashKey, data1))
    set2 = set(map(EqualityHashKey, [[], [1], [2], {}, ()]))
    assert set1 == set2
    assert len(set1) == 5

    # Test that ``EqualityHashKey(item)`` is distinct from ``item``
    T0 = ()
    T1 = (1,)
    data2 = list(map(EqualityHashKey, [T0, T0, T1, T1, (), (1,)]))
    data2.extend([T0, T1, (), (1,)])
    set3 = set(data2)
    assert set3 == set([(), (1,), EqualityHashKey(()), EqualityHashKey((1,))])
    assert len(set3) == 4
    assert EqualityHashKey(()) in set3
    assert EqualityHashKey((1,)) in set3

    # Miscellaneous
    E1 = EqualityHashKey(L1)
    E2 = EqualityHashKey(L2)
    assert str(E1) == '=[1]='
    assert repr(E1) == '=[1]='
    assert E1 != E2
    assert not (E1 == E2)
    assert E1 == EqualityHashKey(L1)
    assert not (E1 != EqualityHashKey(L1))
    assert E1 != L1
    assert not (E1 == L1)
