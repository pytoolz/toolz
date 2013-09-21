from toolz.dicttoolz import merge

def test_merge():
    assert merge({1: 1, 2: 2}, {3: 4}) == {1: 1, 2: 2, 3: 4}
