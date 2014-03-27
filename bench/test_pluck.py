from toolz import pluck

tuples = [(1, 2, 3) for i in range(100000)]


def test_pluck():
    for i in pluck(2, tuples):
        pass
