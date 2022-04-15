from openpipe.shot import create_sequence

import pytest
from pyfakefs.fake_filesystem_unittest import Patcher

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
    pytest.param("ASsc020"),
    pytest.param("SOMEpreviz010"),
])
def test_create_invalid_sequence(monkeypatch, sequence_name):
    monkeypatch.setenv("OPENPIPE_SHOW", "a_test_show")

    with pytest.raises(ValueError):
        with Patcher() as patcher:
            add_openconfig_configs_to_pyfakefs(patcher.fs)
            create_sequence(sequence_name, raise_exc=True)
