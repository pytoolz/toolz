from toolz.itertoolz.recipes import countby


def even(x):
    return x % 2 == 0


def test_countby():
    assert countby(even, [1, 2, 3]) == {True: 1, False: 2}
    assert countby(len, ['cat', 'dog', 'mouse']) == {3: 2, 5: 1}
