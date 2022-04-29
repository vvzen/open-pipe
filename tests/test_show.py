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
        os.makedirs(os.path.join(SHOWS_TMP_ROOT_PATH, show_name))

    if all_steps:
        openpipe.show.create_show(show_name, steps=openpipe.show.ALL_STEPS)
    else:
        openpipe.show.create_show(show_name)

    # Clean up
    shutil.rmtree(SHOWS_TMP_ROOT_PATH)


def test_show_creation_top_directory_exists():
    show_name = "test"

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


@pytest.mark.behaviour_test
@pytest.mark.parametrize("name, steps", [
    pytest.param("some-name", ["some-weird-step"]),
    pytest.param("some-name", ["some-weird-step", "and another one"]),
])
def test_show_creation_wrong_steps(name, steps):
    with pytest.raises(RuntimeError):
        openpipe.show.create_show(name, steps)


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

    openpipe.show.create_show(name)
    openpipe.show.create_show(name)
