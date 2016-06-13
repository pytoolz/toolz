"""``tlz`` mirrors the ``toolz`` API and uses ``cytoolz`` if possible.

The ``tlz`` package is installed when ``toolz`` is installed.  It provides
a convenient way to use functions from ``cytoolz``--a faster Cython
implementation of ``toolz``--if it's installed, otherwise it uses functions
from ``toolz``.
"""

from . import _build_tlz
