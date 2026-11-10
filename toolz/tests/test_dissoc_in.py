from collections import OrderedDict
from types import MappingProxyType

import pytest

from toolz import dicttoolz


@pytest.mark.parametrize('keys', [['outer', 'remove'], ('outer', 'remove'), iter(['outer', 'remove'])])
def test_nested_deletion_does_not_mutate_or_copy_unrelated_values(keys):
    shared = {'value': [1, 2]}
    original = {'outer': {'remove': 1, 'keep': shared}, 'other': shared}
    result = dicttoolz.dissoc_in(original, keys)
    assert result == {'outer': {'keep': shared}, 'other': shared}
    assert original['outer']['remove'] == 1
    assert result is not original
    assert result['outer'] is not original['outer']
    assert result['other'] is shared
    assert result['outer']['keep'] is shared


@pytest.mark.parametrize('keys', [['absent'], ['absent', 'leaf'], ['outer', 'absent']])
def test_missing_paths_do_not_create_keys(keys):
    original = {'outer': {'keep': 1}}
    result = dicttoolz.dissoc_in(original, keys)
    assert result == original
    assert result is not original


def test_empty_parent_is_retained():
    assert dicttoolz.dissoc_in({'a': {'b': 1}}, ['a', 'b']) == {'a': {}}


def test_mapping_inputs_and_factory_preserve_order():
    original = MappingProxyType({'a': MappingProxyType({'first': 1, 'last': 2}), 'z': 3})
    result = dicttoolz.dissoc_in(original, ['a', 'first'], factory=OrderedDict)
    assert isinstance(result, OrderedDict)
    assert isinstance(result['a'], OrderedDict)
    assert list(result) == ['a', 'z']
    assert list(result['a']) == ['last']
    assert original['a']['first'] == 1


def test_empty_path_is_rejected():
    with pytest.raises(ValueError, match='nonempty'):
        dicttoolz.dissoc_in({'a': 1}, [])


def test_nonmapping_intermediate_is_rejected():
    original = {'a': 1}
    with pytest.raises(TypeError, match='mapping'):
        dicttoolz.dissoc_in(original, ['a', 'b'])
    assert original == {'a': 1}


def test_deep_paths_do_not_require_recursion():
    original = {'leaf': 1}
    for _ in range(1500):
        original = {'child': original}
    result = dicttoolz.dissoc_in(original, ['child'] * 1500 + ['leaf'])
    for _ in range(1500):
        result = result['child']
        original = original['child']
    assert result == {}
    assert original == {'leaf': 1}


def test_public_and_curried_namespaces():
    import toolz
    import tlz
    from toolz import curried

    assert toolz.dissoc_in({'a': {'b': 1}}, ['a', 'b']) == {'a': {}}
    assert curried.dissoc_in({'a': {'b': 1}})(['a', 'b']) == {'a': {}}
    assert tlz.dissoc_in({'a': {'b': 1}}, ['a', 'b']) == {'a': {}}
