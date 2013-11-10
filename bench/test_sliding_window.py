from toolz import sliding_window

seq = range(1000000)


def test_sliding_window():
    list(sliding_window(3, seq))
