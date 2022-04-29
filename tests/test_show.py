import os
import shutil

import pytest

from openpipe.show import create_show, ALL_STEPS
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
@pytest.mark.parametrize("show_name, top_dir_already_exists, all_steps", [
    pytest.param("the_witcher_season_3", True, False),
    pytest.param("the latest beautiful commercial", False, False),
    pytest.param("koyaanisqatsi", False, False),
    pytest.param("samsara", False, True),
])
def test_show_creation(monkeypatch,
                       user_reply, show_name, top_dir_already_exists, all_steps):

    # Pretend to be replying to the input() calls
    def mocked_input(*args, **kwargs):
        return user_reply

    def mocked_get_config_path(*args, **kwargs):
        return os.path.join(SAMPLES_DIR, "configs", "sample_openpipe.toml")

    monkeypatch.setattr("builtins.input", mocked_input)
    monkeypatch.setattr("openpipe.config.get_config_path", mocked_get_config_path)

    if not os.path.exists(SHOWS_TMP_ROOT_PATH):
        os.makedirs(SHOWS_TMP_ROOT_PATH)


    if top_dir_already_exists:
        show_path = os.path.join(SHOWS_TMP_ROOT_PATH, show_name)
        if not os.path.exists(show_path):
            os.makedirs(show_path)

    if all_steps:
        create_show(show_name, steps=ALL_STEPS, raise_exc=True)
    else:
        create_show(show_name, raise_exc=True)

    # Clean up
    shutil.rmtree(SHOWS_TMP_ROOT_PATH)


def test_show_creation_top_directory_exists():
    show_name = "test"

    if not os.path.exists(SHOWS_TMP_ROOT_PATH):
        os.makedirs(SHOWS_TMP_ROOT_PATH)

    create_show(show_name)

    # Clean up
    shutil.rmtree(SHOWS_TMP_ROOT_PATH)


@pytest.mark.behaviour_test
@pytest.mark.parametrize("name", [
    pytest.param("show_to_setup_twice"),
])
@pytest.mark.parametrize("user_reply", [
    pytest.param("yes"),
])
def test_show_creation_twice(monkeypatch, name, user_reply):
    # Try setting up the same show twice
    # This helps us to understand how 'idempotent' the show creation really is

    def mocked_input(*args, **kwargs):
        return user_reply

    def mocked_get_config_path(*args, **kwargs):
        return os.path.join(SAMPLES_DIR, "configs", "sample_openpipe.toml")

    monkeypatch.setattr("builtins.input", mocked_input)
    monkeypatch.setattr("openpipe.config.get_config_path", mocked_get_config_path)

    create_show(name)
    create_show(name)

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
        create_show("test")

    # Clean up
    shutil.rmtree(SHOWS_TMP_ROOT_PATH)


@pytest.mark.behaviour_test
@pytest.mark.parametrize("name, steps", [
    pytest.param("some-name", ["some-weird-step"]),
    pytest.param("some-name", ["some-weird-step", "and another one"]),
])
def test_show_creation_wrong_steps(name, steps):
    with pytest.raises(RuntimeError):
        create_show(name, steps)