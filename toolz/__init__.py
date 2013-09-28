from .itertoolz import (groupby, countby, frequencies, reduceby,
        first, second, nth, take, drop, rest, last, get,
        merge_sorted, concat, mapcat,
        interleave, unique, intersection, iterable, distinct)

from .functoolz import (remove, iterate, accumulate,
        memoize, curry, compose,
        thread_first, thread_last)

from .dicttoolz import merge, keymap, valmap, assoc, update_in

# Aliases
comp = compose

__version__ = '0.2'
