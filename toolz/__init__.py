from .itertoolz import (groupby, countby, frequencies, reduceby,
                        first, second, nth, take, drop, rest, last,
                        get, merge_sorted, concat, concatv, mapcat,
                        isdistinct, interleave, unique, intersection,
                        isiterable, remove, iterate, accumulate,
                        partitionby, partition, partition_all,
                        sliding_window, count)

from .functoolz import (memoize, curry, compose, thread_first,
                        thread_last, identity, pipe)

from .dicttoolz import merge, merge_with, keymap, valmap, assoc, update_in

from .compatibility import map, filter

from . import sandbox

from functools import partial, reduce

sorted = sorted

# Aliases
comp = compose

__version__ = '0.4.1'
