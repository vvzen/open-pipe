import pytest

import openpipe.config
from openpipe.config import ConfigNotFoundError


def test_get_config_path_when_missing_env_var(monkeypatch):

    monkeypatch.setenv("OPENPIPE_CONFIG_PATH", "")

    with pytest.raises(EnvironmentError):
        openpipe.config.get_config("some_config_name")


def test_get_config_path_with_nonexistent_config_name():
    with pytest.raises(ConfigNotFoundError):
        openpipe.config.get_config("a_non_existent_config_name")
