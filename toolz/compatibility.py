import sys

PYPY = hasattr(sys, 'pypy_version_info')

__all__ = ('PYPY',)
