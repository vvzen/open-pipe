import pytest
from pyfakefs.fake_filesystem_unittest import Patcher

from openpipe.shot import create_shot, ShotCreationSteps, ALL_STEPS
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
    pytest.param("sc010_0010"),
    pytest.param("sc010_0020"),
    pytest.param("sc020_0010"),
    pytest.param("previz010_0010"),
])
def test_create_shot_all_steps(monkeypatch, shot_name):
    monkeypatch.setenv("OPENPIPE_SHOW", "a_test_show")

    with Patcher() as patcher:
        add_openconfig_configs_to_pyfakefs(patcher.fs)
        create_shot(shot_name, steps=ALL_STEPS, raise_exc=True)

@pytest.mark.parametrize("shot_name, steps", [
    # Only bad steps
    pytest.param("sc010_0010", ["some-funky-step"]),
    # Mix of good and bad steps
    pytest.param("sc020_0010", [ShotCreationSteps.setup_on_disk, "some-funky-step"]),
])
def test_create_shot_wrong_steps(monkeypatch, shot_name, steps):
    monkeypatch.setenv("OPENPIPE_SHOW", "a_test_show")

    with Patcher() as patcher:
        add_openconfig_configs_to_pyfakefs(patcher.fs)

        with pytest.raises(RuntimeError):
            create_shot(shot_name, steps=steps, raise_exc=True)

@pytest.mark.parametrize("shot_name", [
    pytest.param("sc020_000010"),
    pytest.param("SC020_0010"),
    pytest.param("Previz010_0010"),
])
def test_create_invalid_shot(monkeypatch, shot_name):
    monkeypatch.setenv("OPENPIPE_SHOW", "a_test_show")

    with Patcher() as patcher:
        add_openconfig_configs_to_pyfakefs(patcher.fs)

        with pytest.raises(ValueError):
            create_shot(shot_name, raise_exc=True)
