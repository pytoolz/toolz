from toolz.compatibility import map, filter, apply


def test_map_filter_are_lazy():
    def bad(x):
        raise Exception()
    map(bad, [1, 2, 3])
    filter(bad, [1, 2, 3])


def test_apply():
    assert apply(set.union, (set([1]), set([2]))) == \
            set.union(set([1]), set([2]))
