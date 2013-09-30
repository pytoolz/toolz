from toolz.compatibility import map, filter

def test_map_filter_are_lazy():
    def bad(x):
        raise Exception()
    map(bad, [1, 2, 3])
    filter(bad, [1, 2, 3])
