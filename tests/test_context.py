import os

import pytest
from pyfakefs.fake_filesystem_unittest import Patcher

from openpipe.context import make_context_from_path, OpenPipeContext

from conftest import add_openconfig_configs_to_pyfakefs


@pytest.mark.parametrize("path, expected_context", [
    #
    pytest.param("/something/that/is/a/show/sc010/sc010_0010",
                 OpenPipeContext(show="show", sequence="sc010", shot="sc010_0010")),
    #
    pytest.param("/something/that/is/a/show/sc020/sc020_0010",
                 OpenPipeContext(show="show", sequence="sc020", shot="sc020_0010")),
    #
    pytest.param("/something/that/is/a/show/sc010",
                 OpenPipeContext(show="show", sequence="sc010")),
    #
    pytest.param("/a/show/sc010",
                 OpenPipeContext(show="show", sequence="sc010")),
    #
    pytest.param("/a/show/sc010/sc010_0020",
                 OpenPipeContext(show="show", sequence="sc010", shot="sc010_0020")),
    #
    pytest.param("/net/shows/my_very_elaborate_show_name/sc020",
                 OpenPipeContext(show="my_very_elaborate_show_name", sequence="sc020")),
    #
    pytest.param("/net/shows/my_very_elaborate_show_name/sc040/sc040_0050",
                 OpenPipeContext(show="my_very_elaborate_show_name", sequence="sc040", shot="sc040_0050")),
])
def test_make_context_from_path_for_sequences_and_shots(path, expected_context):
    with Patcher() as patcher:
        add_openconfig_configs_to_pyfakefs(patcher.fs)
        assert make_context_from_path(path) == expected_context


@pytest.mark.parametrize("path, with_pipe_directory, expected_context", [
    #
    pytest.param("/net/shows/my_very_elaborate_show_name",
                 True,
                 OpenPipeContext(show="my_very_elaborate_show_name")),
    #
    pytest.param("/net/shows/my_very_elaborate_show_name",
                 False,
                 OpenPipeContext(show=None)),
    #
    pytest.param("/net/shows/nested/my_show_name",
                 True,
                 OpenPipeContext(show="my_show_name")),
])
def test_make_context_from_path_for_show(path, with_pipe_directory, expected_context):

    with Patcher() as patcher:
        add_openconfig_configs_to_pyfakefs(patcher.fs)

        patcher.fs.create_dir(path)

        if with_pipe_directory:
            patcher.fs.create_dir(os.path.join(path, "openpipe", "etc"))

        assert make_context_from_path(path) == expected_context

@pytest.mark.to_test
@pytest.mark.parametrize("path, with_sequence_directory, sequence_name, expected_context", [
    # A valid sequence name
    pytest.param("/net/shows/my_show_name",
                 True,
                 "sc010",
                 OpenPipeContext(show="my_show_name")),
    # An invalid sequence name
    pytest.param("/net/shows/my_show_name",
                 True,
                 "notASequence010",
                 OpenPipeContext(show=None)),
    # No sequence at all and no openpipe/etc dir.
    # We can't know the show name!
    pytest.param("/net/shows/my_very_elaborate_show_name",
                 False,
                 None,
                 OpenPipeContext(show=None)),
])
def test_make_context_from_path_for_show_with_sequences(path, with_sequence_directory, sequence_name, expected_context):

    with Patcher() as patcher:
        add_openconfig_configs_to_pyfakefs(patcher.fs)

        patcher.fs.create_dir(path)

        if with_sequence_directory:
            patcher.fs.create_dir(os.path.join(path, sequence_name))

        assert make_context_from_path(path) == expected_context
