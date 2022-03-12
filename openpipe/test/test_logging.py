from openpipe.logging import get_logger

def test_get_logger_only_returns_one_logger():
    logger_1 = get_logger("my-awesome-logger")
    logger_2 = get_logger("my-awesome-logger")
    assert logger_1 is logger_2

    logger_3 = get_logger("my-other-logger")
    assert logger_1 is not logger_3
