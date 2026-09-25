import pytest
import toolz


def test_pipe_with_kwargs():
    """Test that pipe works with functions that accept **kwargs"""
    some_dict = {"hello": "world", "foo": "bar", "number": 0}

    def first_func(hello, foo, **kwargs):
        hello = "John"
        foo = "baz"
        kwargs['newvalue'] = True
        return kwargs

    def second_func(number, **kwargs):
        number = number + 1
        kwargs['number'] = number
        kwargs['anothervalue'] = False
        return kwargs

    # This should work: piping a dict through functions that use **kwargs
    result = toolz.pipe(some_dict, lambda d: first_func(**d), second_func)

    # Verify the result contains expected values from both functions
    assert result['number'] == 1
    assert result['newvalue'] is True
    assert result['anothervalue'] is False

    # Original dict should remain untouched
    assert some_dict == {"hello": "world", "foo": "bar", "number": 0}
