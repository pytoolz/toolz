from toolz import groupby, identity

data = range(1000)*1000

def test_groupby():
    groupby(identity, data)
