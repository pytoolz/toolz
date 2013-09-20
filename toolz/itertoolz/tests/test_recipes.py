from toolz.itertoolz.recipes import countby, frequencies


def even(x):
    return x % 2 == 0


def test_frequencies():
    assert (frequencies(["cat", "pig", "cat", "eel",
                        "pig", "dog", "dog", "dog"]) ==
            {"cat": 2, "eel": 1, "pig": 2, "dog": 3})
    assert frequencies([]) == {}
    assert frequencies("onomatopoeia") == {"a": 2, "e": 1, "i": 1, "m": 1,
                                           "o": 4, "n": 1, "p": 1, "t": 1}


def test_countby():
    assert countby(even, [1, 2, 3]) == {True: 1, False: 2}
    assert countby(len, ['cat', 'dog', 'mouse']) == {3: 2, 5: 1}
