import copy

import pytest

from openpipe.data import (
    flatten_dict, flatten_list
)

@pytest.mark.behaviour_test
@pytest.mark.parametrize("input_list,expected_result", [
      # Nothing to flatten
      pytest.param([1, 2, 3], [1, 2, 3]),
      # One level of nesting
      pytest.param([1, 2, [3, 4]], [1, 2, 3, 4]),
      # Several levels of nesting
      pytest.param([1, 2, [3, [[4, [5, 6]]]]], [1, 2, 3, 4, 5, 6]),
      # We love tuples, too
      pytest.param((1, 2, (3, ((4, (5, 6))))), [1, 2, 3, 4, 5, 6]),
])
def test_flatten_list(input_list, expected_result):
    original_list = input_list[:]
    assert flatten_list(input_list) == expected_result
    # No side effects should happen
    assert input_list == original_list


@pytest.mark.behaviour_test
@pytest.mark.parametrize("input_dict,expected_result", [
    # Nothing to flatten
    pytest.param(
        { "a": 1, }, { "a": 1 }
    ),
    # One level of nesting
    pytest.param(
        {
            "a": 1,
            "b": { "c": 2 },
        },
        {
            "a": 1,
            "b.c": 2
        }
    ),
    # Several layers of nesting
    pytest.param(
        {
            "a": 1,
            "b": {
                "c": 2,
                "d": {
                    "e": {
                        "f": 5,
                        "g": 6
                    },
                    "h": 7
                }
            },
            "i": 8
        },
        {
            "a": 1,
            "b.c": 2,
            "b.d.e.f": 5,
            "b.d.e.g": 6,
            "b.d.h": 7,
            "i": 8
        }
    ),
])
def test_flatten_dict(input_dict, expected_result):
    original_dict = copy.deepcopy(input_dict)
    assert flatten_dict(input_dict) == expected_result
    # No side effects
    assert input_dict == original_dict
