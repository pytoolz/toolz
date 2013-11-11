from toolz.curried import get


pairs = [(1, 2) for i in range(100000)]


def test_get_curried():
    first = get(0)
    for p in pairs:
        first(p)
