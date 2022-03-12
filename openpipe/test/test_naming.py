import pytest

from openpipe.naming import is_shot, is_sequence

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