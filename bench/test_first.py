from toolz import first, second

pairs = [(1, 2) for i in range(1000000)]


def test_first():
    for p in pairs:
        first(p)


def test_second():
    for p in pairs:
        second(p)
