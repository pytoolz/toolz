from toolz.sandbox.core import jackknife, side_effects


def test_jacknife():
    assert tuple(tuple(x) for x in jackknife([1, 2, 3])) == (
        (2, 3), (1, 3), (1, 2))
    assert tuple(tuple(x) for x in jackknife(iter([1, 2, 3]))) == (
        (2, 3), (1, 3), (1, 2))
    assert tuple(tuple(x) for x in jackknife([1, 2, 3], replace=0)) == (
        (0, 2, 3), (1, 0, 3), (1, 2, 0))
    assert tuple(tuple(x) for x in jackknife([])) == ()
    assert tuple(tuple(x) for x in jackknife([1], replace=0)) == ((0,),)


def test_side_effects():
    results = []
    seq = iter((1, 2, 3))
    seq2 = side_effects(results.append, seq)
    for i in seq2:
        pass
    assert results == [1, 2, 3]
