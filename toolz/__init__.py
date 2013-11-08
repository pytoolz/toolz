from .itertoolz import (groupby, countby, frequencies, reduceby,
                        first, second, nth, take, drop, rest, last,
                        get, merge_sorted, concat, concatv, mapcat,
                        isdistinct, interleave, unique, intersection,
                        isiterable, remove, iterate, accumulate,
                        partitionby, sliding_window, partition,
                        partition_all)

from .functoolz import (memoize, curry, compose, thread_first,
                        thread_last, identity, pipe)

from .dicttoolz import merge, merge_with, keymap, valmap, assoc, update_in

from .compatibility import map, filter

from functools import partial, reduce

sorted = sorted

# Aliases
comp = compose

__version__ = '0.3.0'
