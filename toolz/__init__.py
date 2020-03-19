from .itertoolz import *

from .functoolz import *

from .dicttoolz import *

from .recipes import *

from functools import partial, reduce

sorted = sorted

map = map

filter = filter

# Aliases
comp = compose

from . import curried, exceptions, sandbox

functoolz._sigs.create_signature_registry()

__version__ = '0.10.0'
