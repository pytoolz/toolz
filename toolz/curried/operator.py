from __future__ import absolute_import

import operator

from toolz import curry


# We use a blacklist instead of whitelist because:
#   1. We have more things to include than exclude.
#   2. This gives us access to things like matmul iff we are in Python >=3.5.
no_curry = frozenset((
    'abs',
    'index',
    'inv',
    'invert',
    'neg',
    'not_',
    'pos',
    'truth',
))

locals().update(
    dict((name, curry(f) if name not in no_curry else f)
         for name, f in vars(operator).items() if callable(f)),
)

# Clean up the namespace.
del curry
del no_curry
del operator
