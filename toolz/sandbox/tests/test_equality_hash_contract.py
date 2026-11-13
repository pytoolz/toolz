from toolz.sandbox.core import EqualityHashKey


def test_different_hash_strategies_do_not_compare_equal():
    left = EqualityHashKey(len, [1, 2])
    right = EqualityHashKey(lambda item: 3, [1, 2])
    assert hash(left) != hash(right)
    assert left != right
    assert not (left == right)
    assert len({left, right}) == 2


def test_equivalent_strategies_preserve_equality_and_lookup():
    left = EqualityHashKey(0, [1, 2])
    right = EqualityHashKey(lambda item: item[0], [1, 2])
    assert left == right
    assert not (left != right)
    assert {left: "found"}[right] == "found"


def test_default_keys_keep_unhashable_item_equality():
    left = EqualityHashKey(None, [1, 2])
    same = EqualityHashKey(None, [1, 2])
    different = EqualityHashKey(None, [1, 3])
    assert left == same
    assert hash(left) == hash(same)
    assert left != different


def test_unrelated_operands_can_use_reflected_equality():
    class Reflected:
        def __eq__(self, other):
            return isinstance(other, EqualityHashKey)

    key = EqualityHashKey(None, [1])
    assert key.__eq__(object()) is NotImplemented
    assert key.__ne__(object()) is NotImplemented
    assert key == Reflected()
