from typing import Tuple

from toolz.functoolz import curry
from toolz.compatibility import num_required_args


def test_curry_kwonly():
    @curry
    def f(a, *, b=10):
        return a + b
    b_is_five = f(b=5)

    assert b_is_five(3) == 8


def test_curry_kwoly_star():
    @curry
    def f(a, b, *rest, c=3):
        return ((a + b) * c) + sum(rest)

    assert f(3)(4) == 21
    assert f(c=2)(6)(7) == 26
    assert f(6)(c=2)(7) == 26
    assert f(c=2)(6)(7, 3, 4) == 33


def test_curry_annotations():
    @curry
    def f(a: int, b: float, c: str) -> Tuple[float, str]:
        return a + b, c

    assert f(5)(2.5, 'foo') == (7.5, 'foo')


def test_required_kwonly_args():
    def f(*, a):
        return a

    assert num_required_args(f) == 1


def test_required_args_var_position():
    # Note: The py2 version will still pass this test.
    def f(a, b, *rest):
        pass

    assert num_required_args(f) is None  # Should this be 2?



