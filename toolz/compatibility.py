__all__ = ('PYPY', 'PY3')

import sys

PY3 = True
PYPY = hasattr(sys, 'pypy_version_info')

