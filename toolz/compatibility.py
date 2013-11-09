import sys
PY3 = sys.version_info[0] > 2

if PY3:
    map = map
    filter = filter
    range = range
    zip = zip
    from itertools import zip_longest
else:
    range = xrange
    from itertools import imap as map
    from itertools import ifilter as filter
    from itertools import izip as zip
    from itertools import izip_longest as zip_longest
