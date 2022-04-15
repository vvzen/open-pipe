from openpipe.shot import create_shot

import pytest
from pyfakefs.fake_filesystem_unittest import Patcher

from conftest import add_openconfig_configs_to_pyfakefs


@pytest.mark.parametrize("shot_name", [
    pytest.param("sc010_0010"),
    pytest.param("sc010_0020"),
    pytest.param("sc020_0010"),
    pytest.param("previz010_0010"),
])
def test_create_shot(monkeypatch, shot_name):
    monkeypatch.setenv("OPENPIPE_SHOW", "a_test_show")

    with Patcher() as patcher:
        add_openconfig_configs_to_pyfakefs(patcher.fs)
        create_shot(shot_name, raise_exc=True)


@pytest.mark.parametrize("shot_name", [
    pytest.param("sc020_000010"),
    pytest.param("SC020_0010"),
    pytest.param("Previz010_0010"),
])
def test_create_invalid_shot(monkeypatch, shot_name):
    monkeypatch.setenv("OPENPIPE_SHOW", "a_test_show")

    with pytest.raises(ValueError):
        with Patcher() as patcher:
            add_openconfig_configs_to_pyfakefs(patcher.fs)
            create_shot(shot_name, raise_exc=True)
