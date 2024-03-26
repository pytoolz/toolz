from __future__ import annotations

from enum import Enum
from typing import Any, Callable


def raises(err: type[Exception], lamda: Callable[[], Any]) -> bool:
    try:
        lamda()
        return False
    except err:
        return True


class NoDefaultType(Enum):
    no_default = '__no_default__'


no_default = NoDefaultType.no_default

# no_default = '__no__default__'
# NoDefaultType = Literal['__no__default__']


class NoPadType(Enum):
    no_pad = '__no_pad__'


no_pad = NoPadType.no_pad

# no_pad = '__no__pad__'
# NoPadType = Literal['__no__pad__']
