import sys
PY3 = sys.version_info[0] > 2

if PY3:
    import queue as Queue
    map = map
    filter = filter
    range = range
else:
    import Queue
    range = xrange
    from itertools import imap as map
    from itertools import ifilter as filter
