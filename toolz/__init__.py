from functools import partial, reduce

from .itertoolz import *

from .functoolz import *

from .dicttoolz import *

from .recipes import *

sorted = sorted

map = map

filter = filter

# Aliases
comp = compose

from . import curried, sandbox

from .functoolz import _sigs  # type: ignore[attr-defined]

_sigs.create_signature_registry()

from ._version import __version__
