from toolz import *
import pickle

def test_compose():
    f = compose(str, sum)
    g = pickle.loads(pickle.dumps(f))
    assert f((1, 2)) == g((1, 2))
