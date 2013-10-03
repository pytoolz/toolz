from .itertoolz import (groupby, countby, frequencies, reduceby,
                        first, second, nth, take, drop, rest, last,
                        get, merge_sorted, concat, concatv, mapcat,
                        distinct, interleave, unique, intersection,
                        iterable, remove, iterate, accumulate,
                        partitionby)

from .functoolz import (memoize, curry, compose, thread_first,
                        thread_last, identity)

from .dicttoolz import merge, keymap, valmap, assoc, update_in

from .compatibility import map, filter

from functools import partial, reduce

# Aliases
comp = compose

__version__ = '0.2.2'
