import pickle

from toolz import *


def iseven(x):
    return x % 2 == 0


def isdiv3(x):
    return x % 3 == 0


def test_compose():
    f = compose(str, sum)
    g = pickle.loads(pickle.dumps(f))
    assert f((1, 2)) == g((1, 2))


def test_curry():
    f = curry(map)(str)
    g = pickle.loads(pickle.dumps(f))
    assert list(f((1, 2, 3))) == list(g((1, 2, 3)))


def test_juxt():
    f = juxt(str, int, bool)
    g = pickle.loads(pickle.dumps(f))
    assert f(1) == g(1)
    assert f.funcs == g.funcs


def test_complement():
    f = complement(bool)
    assert f(True) is False
    assert f(False) is True
    g = pickle.loads(pickle.dumps(f))
    assert f(True) == g(True)
    assert f(False) == g(False)


def test_conjunction():
    f = conjunction(iseven, isdiv3)
    assert f(6) is True
    assert f(8) is False
    assert f(9) is False
    g = pickle.loads(pickle.dumps(f))
    assert g(6) is True
    assert g(8) is False
    assert g(9) is False


def test_disjunction():
    f = disjunction(iseven, isdiv3)
    assert f(6) is True
    assert f(7) is False
    assert f(8) is True
    g = pickle.loads(pickle.dumps(f))
    assert g(6) is True
    assert g(7) is False
    assert g(8) is True
