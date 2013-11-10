from toolz.curried import *
a, b, c, d, e, f, g = 'abcdefg'

edges = [(a, b), (b, a), (a, c), (a, d), (d, a), (d, e), (e, f), (d, f),
         (f, d), (d, g), (e, g)]


out_degrees = countby(first,  edges)
# {'a': 3, 'b': 1, 'd': 4, 'e': 2, 'f': 1}

in_degrees = countby(second, edges)
# {'a': 2, 'b': 1, 'c': 1, 'd': 2, 'e': 1, 'f': 2, 'g': 2}


out_neighbors = valmap(comp(tuple, map(second)),
                       groupby(first, edges))
# {'a': ('b', 'c', 'd'),
#  'b': ('a',),
#  'd': ('a', 'e', 'f', 'g'),
#  'e': ('f', 'g'),
#  'f': ('d',)}

in_neighbors = valmap(comp(tuple, map(first)),
                      groupby(second, edges))
# {'a': ('b', 'd'),
#  'b': ('a',),
#  'c': ('a',),
#  'd': ('a', 'f'),
#  'e': ('d',),
#  'f': ('e', 'd'),
#  'g': ('d', 'e')}
