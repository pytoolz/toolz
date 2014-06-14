import copy
from toolz.compatibility import reduce


__all__ = ('assoc_obj', 'update_in_obj', 'get_in_obj')


def assoc_obj(o, attr, value):
    """
    Return a new obj with attr set to value

    Does not modify the initial object.

    >>> class C():
    ...     def __init__(self):
    ...         self.x = 1
    >>> c = C()
    >>> assoc_obj(c, 'x', 2).__dict__
    {'x': 2}
    >>> assoc_obj(c, 'y', 3).__dict__   # doctest: +SKIP
    {'x': 1, 'y': 3}
    """
    new_o = copy.deepcopy(o)
    setattr(new_o, attr, value)
    return new_o


def update_in_obj(o, attrs, func, default=None):
    """ Update value in a (potentially) nested object

    inputs:
    o - object on which to operate
    attrs - list or tuple giving the location of the value to be changed in o
    func - function to operate on that value

    If attrs == [a0, ..., aX] and thread_first(o, (getattr, a0), ...,
    (getattr, aX)) == v, update_in_obj returns a copy of the original object
    with v replaced by func(v), but does not mutate the original object.

    If the current attr is not already in o, and there are no further attrs,
    update_in_obj will set the value of attr to func(default). If there are
    further attrs, however, update_in_obj will raise an AttributeError, rather
    than create nested objects.

    >>> inc = lambda x: x + 1
    >>> class Person():
    ...     def __init__(self, age):
    ...         self.age = age
    >>> class Age():
    ...     def __init__(self, years, days):
    ...         self.years = years
    ...         self.days = days
    >>> alice = Person(Age(30, 100))
    >>> update_in_obj(alice, ['age', 'days'], inc).age.__dict__
    {'days': 101, 'years': 30}
    >>> update_in_obj(alice, ['age', 'hours'], int, default=6.5).age.__dict__
    {'hours': 6, 'days': 100, 'years': 30}
    >>> update_in_obj(alice, ['education', 'college'], str, default='CMU')
    Traceback (most recent call last):
        ...
    AttributeError: Person instance has no attribute 'education'
    """
    assert len(attrs) > 0
    attr, rest = attrs[0], attrs[1:]
    if rest:
        return assoc_obj(o, attr,
                         update_in_obj(getattr(o, attr), rest, func, default))
    else:
        innermost = func(getattr(o, attr, default))
        return assoc_obj(o, attr, innermost)


def get_in_obj(attrs, o, default=None, no_default=False):
    """
    Returns thread_first(o, (getattr, a0), ..., (getattr, aX))
    where [a0, ..., aX] == attrs.

    If thread_first(o, (getattr, a0), ..., (getattr, aX)) cannot be found,
    returns ``default``, unless ``no_default`` is specified, then it
    raises AttributeError.

    ``get_in_obj`` is a generalization of ``getattr`` for nested objects.

    >>> class Person():
    ...     def __init__(self, age):
    ...         self.age = age
    >>> class Age():
    ...     def __init__(self, years, days):
    ...         self.years = years
    ...         self.days = days
    >>> alice = Person(Age(30, 100))
    >>> get_in_obj(['age', 'days'], alice)
    100
    >>> get_in_obj(['age', 'hours'], alice)
    >>> get_in_obj(['age', 'hours'], alice, 4)
    4
    >>> get_in_obj(['occupation'], alice, no_default=True)
    Traceback (most recent call last):
        ...
    AttributeError: Person instance has no attribute 'occupation'

    See Also:
        getattr
    """
    try:
        return reduce(getattr, attrs, o)
    except AttributeError:
        if no_default:
            raise
        return default
