from toolz.sandbox.core import jackknife, do


def test_jacknife():
    assert tuple(tuple(x) for x in jackknife([1, 2, 3])) == (
        (2, 3), (1, 3), (1, 2))
    assert tuple(tuple(x) for x in jackknife(iter([1, 2, 3]))) == (
        (2, 3), (1, 3), (1, 2))
    assert tuple(tuple(x) for x in jackknife([1, 2, 3], replace=0)) == (
        (0, 2, 3), (1, 0, 3), (1, 2, 0))
    assert tuple(tuple(x) for x in jackknife([])) == ()
    assert tuple(tuple(x) for x in jackknife([1], replace=0)) == ((0,),)


def test_do():
    inc = lambda x: x + 1
    assert do(inc, 1) == 1

    log = []
    assert do(log.append, 1) == 1
    assert log == [1]
