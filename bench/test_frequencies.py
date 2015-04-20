from toolz import frequencies, identity


big_data = list(range(1000)) * 1000
small_data = list(range(100))


def test_frequencies():
    frequencies(big_data)


def test_frequencies_small():
    for i in range(1000):
        frequencies(small_data)
