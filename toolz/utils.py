from collections import deque


def consume(seq):
    """Efficently consume an iterable"""
    deque(seq, maxlen=0)


def raises(err, lamda):
    try:
        lamda()
        return False
    except err:
        return True


no_default = '__no__default__'
