from toolz import rolling_partition

seq = range(1000000)

def test_rolling_partition():
    list(rolling_partition(3, seq))
