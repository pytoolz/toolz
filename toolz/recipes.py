from toolz.functoolz import compose
from toolz.compatibility import map


lmap = compose(list, map)
tmap = compose(tuple, map)
