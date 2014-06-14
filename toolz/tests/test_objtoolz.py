from toolz.utils import raises
from toolz.objtoolz import assoc_obj, update_in_obj, get_in_obj


inc = lambda x: x + 1


class C():
    pass


def test_assoc_obj():
    c = C()
    assert assoc_obj(c, "a", 1).__dict__ == {"a": 1}
    c.a = 1
    assert assoc_obj(c, "a", 3).__dict__ == {"a": 3}
    assert assoc_obj(c, "b", 3).__dict__ == {"a": 1, "b": 3}

    # Verify immutability:
    o = C()
    o.x = 1
    assoc_obj(o, 'x', 2)
    assert o.x == 1


def test_update_in_obj():
    c = C()
    c.a = 0
    assert update_in_obj(c, ["a"], inc).__dict__ == {"a": 1}
    c = C()
    c.a = 0
    c.b = 1
    assert update_in_obj(c, ["b"], str).__dict__ == {"a": 0, "b": "1"}
    v = C()
    v.a = 0
    c = C()
    c.t = 1
    c.v = v
    assert update_in_obj(c, ["v", "a"], inc).v.__dict__ == {"a": 1}

    # Handle one missing key.
    c = C()
    assert update_in_obj(c, ["z"], str, None).__dict__ == {"z": "None"}
    assert update_in_obj(c, ["z"], inc, 0).__dict__ == {"z": 1}
    assert update_in_obj(c, ["z"], lambda x: x + "ar",
                         default="b").__dict__ == {"z": "bar"}

    # Allow AttributeError to be thrown if more than one missing key,
    # because we don't know what type of object to create for nesting.
    assert raises(AttributeError,
                  lambda: update_in_obj(c, ["y", "z"], inc, default=0))

    # Verify immutability:
    o = C()
    o.x = 1
    update_in_obj(o, ['x'], inc)
    assert o.x == 1


def test_get_in_obj():
    o = C()
    a = C()
    a.b = 1
    o.a = a
    assert get_in_obj(['a', 'b'], o) == 1
    assert get_in_obj(['a', 'b', 'c'], o, 2) == 2
    assert raises(AttributeError,
                  lambda: get_in_obj(['a', 'b', 'c'], o, no_default=True))
