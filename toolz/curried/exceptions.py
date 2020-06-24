import toolz


__all__ = ['merge_with', 'merge', 'intersect']


@toolz.curry
def merge_with(func, d, *dicts, **kwargs):
    return toolz.merge_with(func, d, *dicts, **kwargs)


@toolz.curry
def merge(d, *dicts, **kwargs):
    return toolz.merge(d, *dicts, **kwargs)


@toolz.curry
def intersect(d, *dicts, **kwargs):
    return toolz.intersect(d, *dicts, **kwargs)


merge_with.__doc__ = toolz.merge_with.__doc__
merge.__doc__ = toolz.merge.__doc__
