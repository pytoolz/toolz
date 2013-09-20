import sys
PY3 = sys.version_info[0] > 2

if PY3:
    import queue as Queue
    imap = map
    range = range
else:
    import Queue
    range = xrange
    from itertools import imap
