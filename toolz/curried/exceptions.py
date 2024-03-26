from __future__ import annotations

from typing import TYPE_CHECKING

import toolz

if TYPE_CHECKING:
    from collections.abc import Mapping, MutableMapping
    from typing import Callable, Sequence, TypeVar

    _S = TypeVar('_S')
    _T = TypeVar('_T')
    _U = TypeVar('_U')

    _DictType = MutableMapping[_S, _T]


__all__ = ['merge_with', 'merge']


@toolz.curry
def merge_with(
    func: Callable[[Sequence[_T]], _U],
    d: Mapping[_S, _T],
    *dicts: Mapping[_S, _T],
    **kwargs: type[_DictType],
) -> _DictType[_S, _U]:
    return toolz.merge_with(func, d, *dicts, **kwargs)


@toolz.curry
def merge(
    d: Mapping[_S, _T],
    *dicts: Mapping[_S, _T],
    **kwargs: type[_DictType],
) -> _DictType[_S, _T]:
    return toolz.merge(d, *dicts, **kwargs)


merge_with.__doc__ = toolz.merge_with.__doc__
merge.__doc__ = toolz.merge.__doc__
