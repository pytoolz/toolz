
def test_map_filter_are_lazy():
    def bad(x):
        raise Exception()
    map(bad, [1, 2, 3])
    filter(bad, [1, 2, 3])


def test_dict_iteration():
    d = {'a': 1, 'b': 2, 'c': 3}
    assert not isinstance(d.items(), list)
    assert not isinstance(d.keys(), list)
    assert not isinstance(d.values(), list)
    assert set(d.items()) == set(d.items())
    assert set(d.keys()) == set(d.keys())
    assert set(d.values()) == set(d.values())
