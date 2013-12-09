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
