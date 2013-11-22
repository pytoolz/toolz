import toolz

__all__ = ['merge_with']

def merge_with(fn, *dicts):
    if len(dicts) == 0:
        raise TypeError()
    else:
        return toolz.merge_with(fn, *dicts)
