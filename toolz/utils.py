from collections import deque


def raises(err, lamda):
    try:
        lamda()
        return False
    except err:
        return True


no_default = '__no__default__'


def consume(seq):
    """ Efficiently consume an iterator"""
    deque(seq, 0)
