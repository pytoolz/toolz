import sys
PY3 = sys.version_info[0] > 2

if PY3:  # pragma: no cover
    map = map
    filter = filter
    range = range
else:
    range = xrange
    from itertools import imap as map
    from itertools import ifilter as filter
