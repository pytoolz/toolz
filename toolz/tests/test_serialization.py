from toolz import *
import pickle


def test_compose():
    f = compose(str, sum)
    g = pickle.loads(pickle.dumps(f))
    assert f((1, 2)) == g((1, 2))


def test_curry():
    f = curry(map)(str)
    g = pickle.loads(pickle.dumps(f))
    assert list(f((1, 2, 3))) == list(g((1, 2, 3)))


def curry_numargs_f(x, *y):
    return x + sum(y)

def curry_numargs_g(x, numargs=10):
    return x + numargs


def test_curry_numargs():
    f = curry_numargs_f
    g = curry_numargs_g

    def dopickle(func):
        return pickle.loads(pickle.dumps(func))

    assert dopickle(curry(f, numargs=2))(1) != 1
    assert dopickle(curry(f, numargs=2))(1, 2) == 3

    assert dopickle(curry(g, 1))() == 11
    assert dopickle(curry(g))(1) == 11
    assert dopickle(curry(g, numargs=1))(1) == 11
    assert dopickle(curry(g, numargs=1))(numargs=2)(1) == 3
    assert dopickle(curry(g, numargs=1)(numargs=2))(1) == 3
    assert dopickle(curry(g))(numargs=1)(1) == 2
    assert dopickle(curry(g)(numargs=1))(1) == 2
    assert dopickle(curry(g))(1, numargs=1) == 2


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
