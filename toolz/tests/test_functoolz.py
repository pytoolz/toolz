import platform


from toolz.functoolz import (thread_first, thread_last, memoize, curry,
                             compose, pipe, complement, do, juxt)
from toolz.functoolz import _num_required_args
from operator import add, mul, itemgetter
from toolz.utils import raises
from functools import partial
from toolz.compatibility import reduce, PY3


def iseven(x):
    return x % 2 == 0


def isodd(x):
    return x % 2 == 1


def inc(x):
    return x + 1


def double(x):
    return 2 * x


def test_thread_first():
    assert thread_first(2) == 2
    assert thread_first(2, inc) == 3
    assert thread_first(2, inc, inc) == 4
    assert thread_first(2, double, inc) == 5
    assert thread_first(2, (add, 5), double) == 14


def test_thread_last():
    assert list(thread_last([1, 2, 3], (map, inc), (filter, iseven))) == [2, 4]
    assert list(thread_last([1, 2, 3], (map, inc), (filter, isodd))) == [3]
    assert thread_last(2, (add, 5), double) == 14


def test_memoize():
    fn_calls = [0]  # Storage for side effects

    def f(x, y):
        """ A docstring """
        fn_calls[0] += 1
        return x + y
    mf = memoize(f)

    assert mf(2, 3) == mf(2, 3)
    assert fn_calls == [1]  # function was only called once
    assert mf.__doc__ == f.__doc__
    assert raises(TypeError, lambda: mf(1, {}))


def test_memoize_kwargs():
    fn_calls = [0]  # Storage for side effects

    def f(x, y=0):
        return x + y

    mf = memoize(f)

    assert mf(1) == f(1)
    assert mf(1, 2) == f(1, 2)
    assert mf(1, y=2) == f(1, y=2)
    assert mf(1, y=3) == f(1, y=3)


def test_memoize_curried():
    @curry
    def f(x, y=0):
        return x + y

    f2 = f(y=1)
    fm2 = memoize(f2)

    assert fm2(3) == f2(3)
    assert fm2(3) == f2(3)


def test_memoize_partial():
    def f(x, y=0):
        return x + y

    f2 = partial(f, y=1)
    fm2 = memoize(f2)

    assert fm2(3) == f2(3)
    assert fm2(3) == f2(3)


def test_memoize_key_signature():
    # Single argument should not be tupled as a key.  No keywords.
    mf = memoize(lambda x: False, cache={1: True})
    assert mf(1) is True
    assert mf(2) is False

    # Single argument must be tupled if signature has varargs.  No keywords.
    mf = memoize(lambda x, *args: False, cache={(1,): True, (1, 2): 2})
    assert mf(1) is True
    assert mf(2) is False
    assert mf(1, 1) is False
    assert mf(1, 2) == 2
    assert mf((1, 2)) is False

    # More than one argument is always tupled.  No keywords.
    mf = memoize(lambda x, y: False, cache={(1, 2): True})
    assert mf(1, 2) is True
    assert mf(1, 3) is False
    assert raises(TypeError, lambda: mf((1, 2)))

    # Nullary function (no inputs) uses empty tuple as the key
    mf = memoize(lambda: False, cache={(): True})
    assert mf() is True

    # Single argument must be tupled if there are keyword arguments, because
    # keyword arguments may be passed as unnamed args.
    mf = memoize(lambda x, y=0: False,
                 cache={((1,), frozenset((('y', 2),))): 2,
                        ((1, 2), None): 3})
    assert mf(1, y=2) == 2
    assert mf(1, 2) == 3
    assert mf(2, y=2) is False
    assert mf(2, 2) is False
    assert mf(1) is False
    assert mf((1, 2)) is False

    # Keyword-only signatures must still have an "args" tuple.
    mf = memoize(lambda x=0: False, cache={(None, frozenset((('x', 1),))): 1,
                                           ((1,), None): 2})
    assert mf() is False
    assert mf(x=1) == 1
    assert mf(1) == 2


def test_memoize_curry_cache():
    @memoize(cache={1: True})
    def f(x):
        return False

    assert f(1) is True
    assert f(2) is False


def test_memoize_key():
    @memoize(key=lambda args, kwargs: args[0])
    def f(x, y, *args, **kwargs):
        return x + y

    assert f(1, 2) == 3
    assert f(1, 3) == 3


def test_curry_simple():
    cmul = curry(mul)
    double = cmul(2)
    assert callable(double)
    assert double(10) == 20
    assert repr(cmul) == repr(mul)

    cmap = curry(map)
    assert list(cmap(inc)([1, 2, 3])) == [2, 3, 4]

    assert raises(TypeError, lambda: curry())
    assert raises(TypeError, lambda: curry({1: 2}))


def test_curry_kwargs():
    def f(a, b, c=10):
        return (a + b) * c

    f = curry(f)
    assert f(1, 2, 3) == 9
    assert f(1)(2, 3) == 9
    assert f(1, 2) == 30
    assert f(1, c=3)(2) == 9
    assert f(c=3)(1, 2) == 9

    def g(a=1, b=10, c=0):
        return a + b + c

    cg = curry(g, b=2)
    assert cg() == 3
    assert cg(b=3) == 4
    assert cg(a=0) == 2
    assert cg(a=0, b=1) == 1
    assert cg(0) == 2  # pass "a" as arg, not kwarg
    assert raises(TypeError, lambda: cg(1, 2))  # pass "b" as arg AND kwarg

    def h(x, func=int):
        return func(x)

    if platform.python_implementation() != 'PyPy'\
            or platform.python_version_tuple()[0] != '3':  # Bug on PyPy3<2.5
        # __init__ must not pick func as positional arg
        assert curry(h)(0.0) == 0
        assert curry(h)(func=str)(0.0) == '0.0'
        assert curry(h, func=str)(0.0) == '0.0'


def test_curry_passes_errors():
    @curry
    def f(a, b):
        if not isinstance(a, int):
            raise TypeError()
        return a + b

    assert f(1, 2) == 3
    assert raises(TypeError, lambda: f('1', 2))
    assert raises(TypeError, lambda: f('1')(2))
    assert raises(TypeError, lambda: f(1, 2, 3))


def test_curry_docstring():
    def f(x, y):
        """ A docstring """
        return x

    g = curry(f)
    assert g.__doc__ == f.__doc__
    assert str(g) == str(f)
    assert f(1, 2) == g(1, 2)


def test_curry_is_like_partial():
    def foo(a, b, c=1):
        return a + b + c

    p, c = partial(foo, 1, c=2), curry(foo)(1, c=2)
    assert p.keywords == c.keywords
    assert p.args == c.args
    assert p(3) == c(3)

    p, c = partial(foo, 1), curry(foo)(1)
    assert p.keywords == c.keywords
    assert p.args == c.args
    assert p(3) == c(3)
    assert p(3, c=2) == c(3, c=2)

    p, c = partial(foo, c=1), curry(foo)(c=1)
    assert p.keywords == c.keywords
    assert p.args == c.args
    assert p(1, 2) == c(1, 2)


def test_curry_is_idempotent():
    def foo(a, b, c=1):
        return a + b + c

    f = curry(foo, 1, c=2)
    g = curry(f)
    assert isinstance(f, curry)
    assert isinstance(g, curry)
    assert not isinstance(g.func, curry)
    assert not hasattr(g.func, 'func')
    assert f.func == g.func
    assert f.args == g.args
    assert f.keywords == g.keywords


def test_curry_attributes_readonly():
    def foo(a, b, c=1):
        return a + b + c

    f = curry(foo, 1, c=2)
    assert raises(AttributeError, lambda: setattr(f, 'args', (2,)))
    assert raises(AttributeError, lambda: setattr(f, 'keywords', {'c': 3}))
    assert raises(AttributeError, lambda: setattr(f, 'func', f))


def test_curry_attributes_writable():
    def foo(a, b, c=1):
        return a + b + c

    f = curry(foo, 1, c=2)
    f.__name__ = 'newname'
    f.__doc__ = 'newdoc'
    assert f.__name__ == 'newname'
    assert f.__doc__ == 'newdoc'
    if hasattr(f, 'func_name'):
        assert f.__name__ == f.func_name


def test_curry_comparable():
    def foo(a, b, c=1):
        return a + b + c
    f1 = curry(foo, 1, c=2)
    f2 = curry(foo, 1, c=2)
    g1 = curry(foo, 1, c=3)
    h1 = curry(foo, c=2)
    h2 = h1(c=2)
    h3 = h1()
    assert f1 == f2
    assert not (f1 != f2)
    assert f1 != g1
    assert not (f1 == g1)
    assert f1 != h1
    assert h1 == h2
    assert h1 == h3

    # test function comparison works
    def bar(a, b, c=1):
        return a + b + c
    b1 = curry(bar, 1, c=2)
    assert b1 != f1

    assert set([f1, f2, g1, h1, h2, h3, b1, b1()]) == set([f1, g1, h1, b1])

    # test unhashable input
    unhash1 = curry(foo, [])
    assert raises(TypeError, lambda: hash(unhash1))
    unhash2 = curry(foo, c=[])
    assert raises(TypeError, lambda: hash(unhash2))


def test_curry_doesnot_transmogrify():
    # Early versions of `curry` transmogrified to `partial` objects if
    # only one positional argument remained even if keyword arguments
    # were present.  Now, `curry` should always remain `curry`.
    def f(x, y=0):
        return x + y

    cf = curry(f)
    assert cf(y=1)(y=2)(y=3)(1) == f(1, 3)


def test_curry_on_classmethods():
    class A(object):
        BASE = 10

        def __init__(self, base):
            self.BASE = base

        @curry
        def addmethod(self, x, y):
            return self.BASE + x + y

        @classmethod
        @curry
        def addclass(cls, x, y):
            return cls.BASE + x + y

        @staticmethod
        @curry
        def addstatic(x, y):
            return x + y

    a = A(100)
    assert a.addmethod(3, 4) == 107
    assert a.addmethod(3)(4) == 107
    assert A.addmethod(a, 3, 4) == 107
    assert A.addmethod(a)(3)(4) == 107

    assert a.addclass(3, 4) == 17
    assert a.addclass(3)(4) == 17
    assert A.addclass(3, 4) == 17
    assert A.addclass(3)(4) == 17

    assert a.addstatic(3, 4) == 7
    assert a.addstatic(3)(4) == 7
    assert A.addstatic(3, 4) == 7
    assert A.addstatic(3)(4) == 7

    # we want this to be of type curry
    assert isinstance(a.addmethod, curry)
    assert isinstance(A.addmethod, curry)


def test_memoize_on_classmethods():
    class A(object):
        BASE = 10
        HASH = 10

        def __init__(self, base):
            self.BASE = base

        @memoize
        def addmethod(self, x, y):
            return self.BASE + x + y

        @classmethod
        @memoize
        def addclass(cls, x, y):
            return cls.BASE + x + y

        @staticmethod
        @memoize
        def addstatic(x, y):
            return x + y

        def __hash__(self):
            return self.HASH

    a = A(100)
    assert a.addmethod(3, 4) == 107
    assert A.addmethod(a, 3, 4) == 107

    a.BASE = 200
    assert a.addmethod(3, 4) == 107
    a.HASH = 200
    assert a.addmethod(3, 4) == 207

    assert a.addclass(3, 4) == 17
    assert A.addclass(3, 4) == 17
    A.BASE = 20
    assert A.addclass(3, 4) == 17
    A.HASH = 20  # hashing of class is handled by metaclass
    assert A.addclass(3, 4) == 17  # hence, != 27

    assert a.addstatic(3, 4) == 7
    assert A.addstatic(3, 4) == 7


def test__num_required_args():
    assert _num_required_args(map) != 0
    assert _num_required_args(lambda x: x) == 1
    assert _num_required_args(lambda x, y: x) == 2

    def foo(x, y, z=2):
        pass
    assert _num_required_args(foo) == 2


def test_compose():
    assert compose()(0) == 0
    assert compose(inc)(0) == 1
    assert compose(double, inc)(0) == 2
    assert compose(str, iseven, inc, double)(3) == "False"
    assert compose(str, add)(1, 2) == '3'

    def f(a, b, c=10):
        return (a + b) * c

    assert compose(str, inc, f)(1, 2, c=3) == '10'


def test_pipe():
    assert pipe(1, inc) == 2
    assert pipe(1, inc, inc) == 3
    assert pipe(1, double, inc, iseven) is False


def test_complement():
    # No args:
    assert complement(lambda: False)()
    assert not complement(lambda: True)()

    # Single arity:
    assert complement(iseven)(1)
    assert not complement(iseven)(2)
    assert complement(complement(iseven))(2)
    assert not complement(complement(isodd))(2)

    # Multiple arities:
    both_even = lambda a, b: iseven(a) and iseven(b)
    assert complement(both_even)(1, 2)
    assert not complement(both_even)(2, 2)

    # Generic truthiness:
    assert complement(lambda: "")()
    assert complement(lambda: 0)()
    assert complement(lambda: None)()
    assert complement(lambda: [])()

    assert not complement(lambda: "x")()
    assert not complement(lambda: 1)()
    assert not complement(lambda: [1])()


def test_do():
    inc = lambda x: x + 1
    assert do(inc, 1) == 1

    log = []
    assert do(log.append, 1) == 1
    assert log == [1]


def test_juxt_generator_input():
    data = list(range(10))
    juxtfunc = juxt(itemgetter(2*i) for i in range(5))
    assert juxtfunc(data) == (0, 2, 4, 6, 8)
    assert juxtfunc(data) == (0, 2, 4, 6, 8)
