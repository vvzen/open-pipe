import pytest

import openpipe.log


def test_get_logger_only_returns_one_logger():
    logger_1 = openpipe.log.get_logger("my-awesome-logger")
    logger_2 = openpipe.log.get_logger("my-awesome-logger")
    assert logger_1 is logger_2

    logger_3 = openpipe.log.get_logger("my-other-logger")
    assert logger_1 is not logger_3


@pytest.mark.smoke_test
@pytest.mark.parametrize("env_var_value", [
    pytest.param("DEBUG"),
    pytest.param("INFO"),
    pytest.param("WARNING"),
    pytest.param("DEBUG %(asctime)s-%(filename)s:"),
])
def test_logging_with_custom_env_vars(monkeypatch, env_var_value):
    monkeypatch.setenv("OPENPIPE_LOG", env_var_value)
    log = openpipe.log.get_logger("my-logger")
    log.debug("Something debug worthy")
    log.info("Something of general use")
