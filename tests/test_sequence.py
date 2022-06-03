import pytest
from pyfakefs.fake_filesystem_unittest import Patcher

from openpipe.sequence import create_sequence, SequenceCreationSteps, ALL_STEPS
from conftest import add_openconfig_configs_to_pyfakefs


@pytest.mark.parametrize("sequence_name", [
    pytest.param("sc010"),
    pytest.param("sc010"),
    pytest.param("sc020"),
    pytest.param("previz010"),
])
def test_create_sequence(monkeypatch, sequence_name):
    monkeypatch.setenv("OPENPIPE_SHOW", "a_test_show")

    with Patcher() as patcher:
        add_openconfig_configs_to_pyfakefs(patcher.fs)
        create_sequence(sequence_name, raise_exc=True)

@pytest.mark.parametrize("sequence_name", [
    pytest.param("sc010"),
    pytest.param("sc010"),
    pytest.param("sc020"),
    pytest.param("previz010"),
])
def test_create_sequence_all_steps(monkeypatch, sequence_name):
    monkeypatch.setenv("OPENPIPE_SHOW", "a_test_show")

    with Patcher() as patcher:
        add_openconfig_configs_to_pyfakefs(patcher.fs)
        create_sequence(sequence_name, steps=ALL_STEPS, raise_exc=True)


@pytest.mark.parametrize("sequence_name, steps", [
    # Only bad steps
    pytest.param("sc010", ["some-funky-step"]),
    # Mix of good and bad steps
    pytest.param("sc020", [SequenceCreationSteps.setup_on_disk, "some-funky-step"]),
])
def test_create_sequence_wrong_steps(monkeypatch, sequence_name, steps):
    monkeypatch.setenv("OPENPIPE_SHOW", "a_test_show")

    with Patcher() as patcher:
        add_openconfig_configs_to_pyfakefs(patcher.fs)

        with pytest.raises(RuntimeError):
            create_sequence(sequence_name, steps=steps, raise_exc=True)


@pytest.mark.parametrize("sequence_name", [
    pytest.param("ASsc020"),
    pytest.param("SOMEpreviz010"),
])
def test_create_invalid_sequence(monkeypatch, sequence_name):
    monkeypatch.setenv("OPENPIPE_SHOW", "a_test_show")

    with Patcher() as patcher:
        add_openconfig_configs_to_pyfakefs(patcher.fs)
        with pytest.raises(ValueError):
            create_sequence(sequence_name, raise_exc=True)
