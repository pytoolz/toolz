import toolz


def merge_with(fn, *dicts):
    if len(dicts) == 0:
        raise TypeError()
    else:
        return toolz.merge_with(fn, *dicts)


merge_with.__doc__ = toolz.merge_with.__doc__
