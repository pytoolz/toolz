from toolz.recipes import lmap, tmap


def inc(x):
    return x + 1


def test_lmap():
    assert lmap(inc, (1, 2, 3)) == [2, 3, 4]


def test_tmap():
    assert tmap(inc, (1, 2, 3)) == (2, 3, 4)
