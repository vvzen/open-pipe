# -*- coding: utf-8 -*-
import pytest

from openpipe.sanitization.core import name_for_filesystem


@pytest.mark.parametrize("input_name, output_name", [
    pytest.param("Name with Spaces", "name_with_spaces"),
    pytest.param(u"Something fishy 🐠", "something_fishy_"),
    pytest.param("A_NAME_LIKE_THIS", "a_name_like_this"),
    pytest.param("rm ***/**", "rm_"),
    pytest.param("rm -rf *", "rm__rf_"),
    pytest.param("some-name", "some_name"),
])
def test_name_for_filesystem_expected_input(input_name, output_name):
    assert name_for_filesystem(input_name) == output_name


@pytest.mark.parametrize("input_name", [
    pytest.param(["something"]),
    pytest.param({"some_name": "some_value"}),
    pytest.param(bytes("something", "ascii")),
])
def test_name_for_filesystem_wrong_inputs(input_name):
    with pytest.raises(TypeError):
        name_for_filesystem(input_name)
