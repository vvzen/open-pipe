import os
import shutil

import pytest

import openpipe.show
import openpipe.config
from conftest import (SAMPLES_DIR)
SHOWS_TMP_ROOT_PATH = "/tmp/openpipe/shows"
SAMPLE_CONFIGS_DIR = os.path.join(SAMPLES_DIR, "configs")

@pytest.mark.behaviour_test
@pytest.mark.parametrize("user_reply", [
    pytest.param("yes"),
    pytest.param("y"),
    pytest.param("n"),
    pytest.param("no"),
])
@pytest.mark.parametrize("show_name", [
    pytest.param("the_witcher_season_3"),
    pytest.param("the latest beautiful commercial"),
    pytest.param("koyaanisqatsi"),
])
def test_show_creation(monkeypatch, user_reply, show_name):

    # Pretend to be replying to the input() calls
    def mocked_input(*args, **kwargs):
        return user_reply

    def mocked_get_config_path(*args, **kwargs):
        return os.path.join(SAMPLES_DIR, "configs", "sample_openpipe.toml")

    monkeypatch.setattr("builtins.input", mocked_input)
    monkeypatch.setattr("openpipe.config.get_config_path", mocked_get_config_path)

    if not os.path.exists(SHOWS_TMP_ROOT_PATH):
        os.makedirs(SHOWS_TMP_ROOT_PATH)

    openpipe.show.create_show(show_name)

    # Clean up
    shutil.rmtree(SHOWS_TMP_ROOT_PATH)

@pytest.mark.behaviour_test
@pytest.mark.parametrize("config_path", [
    pytest.param(os.path.join(SAMPLE_CONFIGS_DIR, "wrong_openpipe_missing_root_path.toml")),
    pytest.param(os.path.join(SAMPLE_CONFIGS_DIR, "wrong_openpipe_missing_show_key.toml"))
])
def test_show_creation_wrong_openpipe_configs(monkeypatch, config_path):

    # Pretend to be replying 'yes' to the input() calls
    def mocked_input(*args, **kwargs):
        return "y"

    def mocked_get_config_path(*args, **kwargs):
        return config_path

    monkeypatch.setattr("builtins.input", mocked_input)
    monkeypatch.setattr("openpipe.config.get_config_path", mocked_get_config_path)

    if not os.path.exists(SHOWS_TMP_ROOT_PATH):
        os.makedirs(SHOWS_TMP_ROOT_PATH)

    with pytest.raises(openpipe.config.MalformedConfigError):
        openpipe.show.create_show("test")

    # Clean up
    shutil.rmtree(SHOWS_TMP_ROOT_PATH)