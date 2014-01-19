from toolz import frequencies, identity

data = range(1000)*1000

def test_frequencies():
    frequencies(data)
