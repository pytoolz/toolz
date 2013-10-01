import itertools
from toolz.utils import raises
from functools import partial
from toolz.itertoolz.core import (remove, groupby, merge_sorted,
                                  concat, concatv, interleave, unique,
                                  identity, intersection, iterable,
                                  mapcat, distinct, first, second,
                                  nth, take, drop, interpose, get,
                                  rest, last, cons, frequencies, reduceby,
                                  iterate, accumulate)
from toolz.compatibility import range
from operator import add, mul


def even(x):
    return x % 2 == 0


def odd(x):
    return x % 2 == 1


def inc(x):
    return x + 1


def double(x):
    return 2 * x


def test_remove():
    assert list(remove(even, range(5))) == list(filter(odd, range(5)))


def test_groupby():
    assert groupby(even, [1, 2, 3, 4]) == {True: [2, 4], False: [1, 3]}


def test_merge_sorted():
    assert list(merge_sorted([1, 2, 3], [1, 2, 3])) == [1, 1, 2, 2, 3, 3]
    assert list(merge_sorted([1, 3, 5], [2, 4, 6])) == [1, 2, 3, 4, 5, 6]
    assert list(merge_sorted([1], [2, 4], [3], [])) == [1, 2, 3, 4]


def test_interleave():
    assert ''.join(interleave(('ABC', '123'))) == 'A1B2C3'
    assert ''.join(interleave(('ABC', '1'))) == 'A1BC'


def test_unique():
    assert tuple(unique((1, 2, 3))) == (1, 2, 3)
    assert tuple(unique((1, 2, 1, 3))) == (1, 2, 3)
    assert tuple(unique((1, 2, 3), key=even)) == (1, 2)


def test_intersection():
    assert list(intersection([1, 2, 3], [2, 3, 4])) == [2, 3]
    assert list(intersection([3, 4], itertools.count(0))) == [3, 4]


def test_iterable():
    assert iterable([1, 2, 3]) == True
    assert iterable('abc') == True
    assert iterable(5) == False


def test_distinct():
    assert distinct([1, 2, 3]) == True
    assert distinct([1, 2, 1]) == False

    assert distinct("Hello") == False
    assert distinct("World") == True


def test_nth():
    assert nth(2, 'ABCDE') == 'C'
    assert nth(1, (3, 2, 1)) == 2


def test_first():
    assert first('ABCDE') == 'A'
    assert first((3, 2, 1)) == 3


def test_second():
    assert second('ABCDE') == 'B'
    assert second((3, 2, 1)) == 2


def test_last():
    assert last('ABCDE') == 'E'
    assert last((3, 2, 1)) == 1


def test_rest():
    assert list(rest('ABCDE')) == list('BCDE')
    assert list(rest((3, 2, 1))) == list((2, 1))


def test_take():
    assert list(take(3, 'ABCDE')) == list('ABC')
    assert list(take(2, (3, 2, 1))) == list((3, 2))


def test_drop():
    assert list(drop(3, 'ABCDE')) == list('DE')
    assert list(drop(1, (3, 2, 1))) == list((2, 1))


def test_get():
    assert get(1, 'ABCDE') == 'B'
    assert list(get([1, 3], 'ABCDE')) == list('BD')
    assert get('a', {'a': 1, 'b': 2, 'c': 3}) == 1
    assert get(['a', 'b'], {'a': 1, 'b': 2, 'c': 3}) == (1, 2)

    assert get('foo', {}, default='bar') == 'bar'

    assert raises(IndexError, lambda: get(10, 'ABC'))
    assert raises(KeyError, lambda: get(10, {'a': 1}))


def test_mapcat():
    assert (list(mapcat(identity, [[1, 2, 3], [4, 5, 6]])) ==
            [1, 2, 3, 4, 5, 6])

    assert (list(mapcat(reversed, [[3, 2, 1, 0], [6, 5, 4], [9, 8, 7]])) ==
            list(range(10)))

    inc = lambda i: i + 1
    assert ([4, 5, 6, 7, 8, 9] ==
            list(mapcat(partial(map, inc), [[3, 4, 5], [6, 7, 8]])))


def test_cons():
    assert list(cons(1, [2, 3])) == [1, 2, 3]


def test_concat():
    assert list(concat([[], [], []])) == []
    assert (list(take(5, concat([['a', 'b'], range(1000000000)]))) ==
            ['a', 'b', 0, 1, 2])


def test_concatv():
    assert list(concatv([], [], [])) == []
    assert (list(take(5, concatv(['a', 'b'], range(1000000000)))) ==
            ['a', 'b', 0, 1, 2])


def test_interpose():
    assert "a" == first(rest(interpose("a", range(10000000000))))
    assert "tXaXrXzXaXn" == "".join(interpose("X", "tarzan"))


def test_frequencies():
    assert (frequencies(["cat", "pig", "cat", "eel",
                        "pig", "dog", "dog", "dog"]) ==
            {"cat": 2, "eel": 1, "pig": 2, "dog": 3})
    assert frequencies([]) == {}
    assert frequencies("onomatopoeia") == {"a": 2, "e": 1, "i": 1, "m": 1,
                                           "o": 4, "n": 1, "p": 1, "t": 1}


def test_reduceby():
    data = [1, 2, 3, 4, 5]
    iseven = lambda x: x % 2 == 0
    assert reduceby(iseven, add, data, 0) == {False: 9, True: 6}
    assert reduceby(iseven, mul, data, 1) == {False: 15, True: 8}

    projects = [{'name': 'build roads', 'state': 'CA', 'cost': 1000000},
                {'name': 'fight crime', 'state': 'IL', 'cost': 100000},
                {'name': 'help farmers', 'state': 'IL', 'cost': 2000000},
                {'name': 'help farmers', 'state': 'CA', 'cost': 200000}]
    assert reduceby(lambda x: x['state'],
                    lambda acc, x: acc + x['cost'],
                    projects, 0) == {'CA': 1200000, 'IL': 2100000}


def test_iterate():
    assert list(itertools.islice(iterate(inc, 0), 0, 5)) == [0, 1, 2, 3, 4]


def test_accumulate():
    assert list(accumulate(add, [1, 2, 3, 4, 5])) == [1, 3, 6, 10, 15]
    assert list(accumulate(mul, [1, 2, 3, 4, 5])) == [1, 2, 6, 24, 120]
