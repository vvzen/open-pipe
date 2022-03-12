import pytest

from openpipe.context import make_context_from_path, OpenPipeContext

@pytest.mark.parametrize("path, expected_context", [
    #
    pytest.param("/something/that/is/a/show/sc010/sc010_0010",
                 OpenPipeContext(show="show", sequence="sc010", shot="sc010_0010")),
    #
    pytest.param("/something/that/is/a/show/sc020/sc020_0010",
                 OpenPipeContext(show="show", sequence="sc020", shot="sc020_0010")),
    #
    pytest.param("/something/that/is/a/show/sc010",
                 OpenPipeContext(show="show", sequence="sc010", shot=None)),
    #
    pytest.param("/a/show/sc010",
                 OpenPipeContext(show="show", sequence="sc010", shot=None)),
    #
    pytest.param("/a/show/sc010/sc010_0020",
                 OpenPipeContext(show="show", sequence="sc010", shot="sc010_0020")),
    #
    pytest.param("/net/shows/my_very_elaborate_show_name/sc020",
                 OpenPipeContext(show="my_very_elaborate_show_name", sequence="sc020", shot=None)),
    #
    pytest.param("/net/shows/my_very_elaborate_show_name/sc040/sc040_0050",
                 OpenPipeContext(show="my_very_elaborate_show_name", sequence="sc040", shot="sc040_0050")),
])
def test_make_context_from_path(path, expected_context):
    assert make_context_from_path(path) == expected_context
