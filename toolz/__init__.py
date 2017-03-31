from .itertoolz import *

from .functoolz import *

from .dicttoolz import *

from .objtoolz import *

from .recipes import *

from .compatibility import map, filter

from . import sandbox

from functools import partial, reduce

sorted = sorted

# Aliases
comp = compose

functoolz._sigs.create_signature_registry()

__version__ = '0.8.2'
