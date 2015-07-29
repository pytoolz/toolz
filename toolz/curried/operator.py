import operator as _operator
from test.support import import_fresh_module

from toolz import curry
from .core import should_curry

# Potentially defined in C and _should_curry will fail.
_operator = vars(_operator)
# The pure python implementations.
# We will use these to inspect the call signatures of the C versions.
_pyoperator = vars(import_fresh_module('operator', blocked=['_operator']))

locals().update(
    dict((name, curry(_operator[name])
          if should_curry(pyfunc) else _operator[name])
         for name, pyfunc in _pyoperator.items()),
)

# Clean up the namespace.
del _operator
del _pyoperator
del curry
del import_fresh_module
del should_curry
