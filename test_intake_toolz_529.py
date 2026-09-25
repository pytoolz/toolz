import pytest
from toolz import assoc_in


def test_mapacc_combination_of_map_and_accumulate():
    """Test that mapacc function exists and works as expected"""
    # Import should fail if mapacc doesn't exist
    from toolz import mapacc

    data = [{'id': 'a', 'value': 1},
            {'id': 'b', 'value': 2},
            {'id': 'c', 'value': 3},
            {'id': 'd', 'value': 4}]

    result, acc_values = mapacc(
        mapper=lambda acc, elem: assoc_in(elem, ['value'], max(elem['value'] - acc, 0)),
        accumulator=lambda acc, elem: max(acc - elem['value'], 0),
        sequence=data,
        accumulator_init=4
    )

    expected_result = (
        {'id': 'a', 'value': 0},
        {'id': 'b', 'value': 0},
        {'id': 'c', 'value': 2},
        {'id': 'd', 'value': 4}
    )
    expected_acc = (3, 1, 0, 0)

    assert result == expected_result
    assert acc_values == expected_acc
