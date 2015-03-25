import toolz


def merge_with(fn, *dicts, **kwargs):
    if len(dicts) == 0:
        raise TypeError()
    else:
        return toolz.merge_with(fn, *dicts, **kwargs)


def merge(*dicts, **kwargs):
    if len(dicts) == 0:
        raise TypeError()
    else:
        return toolz.merge(*dicts, **kwargs)

merge_with.__doc__ = toolz.merge_with.__doc__
merge.__doc__ = toolz.merge.__doc__
