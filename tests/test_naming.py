import os

import pytest

import openpipe.config
from openpipe.naming import (
    is_shot, is_sequence,
    sequence_name_from_shot_name, get_naming_regexes
)


CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
SAMPLES_DIR = os.path.join(CURRENT_DIR, "sample_files")


@pytest.mark.parametrize("name,result", [
    pytest.param("sc010_0010", True),
    pytest.param("sc020_0010", True),
    pytest.param("sc010_0040", True),
    pytest.param("previz010_0010", True),
    pytest.param("sc10_0010", False),
    pytest.param("0010", False),
    pytest.param("previz_0010", False),
])
def test_is_shot_with_default_config(name, result):
    assert is_shot(name) == result

@pytest.mark.parametrize("name,result", [
    pytest.param("sc010", True),
    pytest.param("sc120", True),
    pytest.param("sc001", True),
    pytest.param("previz010", True),
    pytest.param("0010", False),
    pytest.param("previz_0010", False),
])
def test_is_sequence_with_default_config(name, result):
    assert is_sequence(name) == result


@pytest.mark.parametrize("config_path", [
    pytest.param(os.path.join(SAMPLES_DIR, "configs", "show_naming_compound_undefined_patterns.toml")),
    pytest.param(os.path.join(SAMPLES_DIR, "configs", "show_naming_missing_shot_pattern.toml")),
    pytest.param(os.path.join(SAMPLES_DIR, "configs", "show_naming_missing_appends_with.toml")),
])
def test_naming_of_malformed_configs(monkeypatch, config_path):

    def mocked_config_path(name):
        return config_path

    monkeypatch.setattr(openpipe.config, "get_config_path", mocked_config_path)

    with pytest.raises(openpipe.config.MalformedConfigError):
        is_shot("name is irrelevant here")


def test_get_naming_regexes_missing_entry():
    assert get_naming_regexes("a_name_that_is_not_a_valid_key") is None


@pytest.mark.parametrize("shot_name, expected_sequence_name", [
    pytest.param("sc010_0010", "sc010"),
    pytest.param("sc020_0010", "sc020"),
    pytest.param("sc030_0040", "sc030"),
    pytest.param("sc020_0040", "sc020"),
    pytest.param("previz010_0010", "previz010"),
])
def test_sequence_name_from_shot_name(shot_name, expected_sequence_name):
    assert sequence_name_from_shot_name(shot_name) == expected_sequence_name

@pytest.mark.parametrize("shot_name", [
    pytest.param("not a shot name"),
    pytest.param("somethingsc020_0010"),
    pytest.param("sc030_0040asdasdasd"),
])
def test_sequence_name_from_invalid_shot_name(shot_name):
    with pytest.raises(ValueError):
        sequence_name_from_shot_name(shot_name)
