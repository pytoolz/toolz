import operator
import sys
PY3 = sys.version_info[0] > 2

__all__ = ('PY3', 'map', 'filter', 'range', 'zip', 'reduce', 'zip_longest',
           'iteritems', 'iterkeys', 'itervalues', 'filterfalse')

if PY3:
    map = map
    filter = filter
    range = range
    zip = zip
    from functools import reduce
    from itertools import zip_longest
    from itertools import filterfalse
    iteritems = operator.methodcaller('items')
    iterkeys = operator.methodcaller('keys')
    itervalues = operator.methodcaller('values')
else:
    range = xrange
    reduce = reduce
    from itertools import imap as map
    from itertools import ifilter as filter
    from itertools import ifilterfalse as filterfalse
    from itertools import izip as zip
    from itertools import izip_longest as zip_longest
    iteritems = operator.methodcaller('iteritems')
    iterkeys = operator.methodcaller('iterkeys')
    itervalues = operator.methodcaller('itervalues')
