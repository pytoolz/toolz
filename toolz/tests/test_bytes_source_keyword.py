"""AI-assisted regressions for builtin source keyword signatures."""

import pytest

from toolz import curry
from toolz.functoolz import is_partial_args, is_valid_args


@pytest.mark.parametrize('constructor', [bytes, bytearray])
@pytest.mark.parametrize('validate', [is_valid_args, is_partial_args])
def test_source_keyword_validation(constructor, validate):
    kwargs = {'source': 'abc', 'encoding': 'utf8'}
    expected = constructor('abc', encoding='utf8')
    assert constructor(**kwargs) == expected
    assert validate(constructor, (), kwargs) is True


@pytest.mark.parametrize('constructor', [bytes, bytearray])
def test_source_keyword_staged_curry(constructor):
    expected = constructor(source='abc', encoding='utf8')
    staged = curry(constructor)(source='abc')
    assert staged(encoding='utf8') == expected
