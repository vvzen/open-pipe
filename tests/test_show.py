import pytest

import openpipe.show

@pytest.mark.parametrize("show_name", [
    pytest.param("the_witcher_season_3"),
    pytest.param("the latest beautiful commercial"),
    pytest.param("koyaanisqatsi"),
])
def test_show_creation(fs, monkeypatch, show_name):

    # NB: fs is the pyfakefs fixture used to get a fake filesystem
    fs.add_real_directory(openpipe.show.CURRENT_DIR)

    # Pretend to be replying 'yes' to the input() calls
    def mocked_input(*args, **kwargs):
        return "y"

    monkeypatch.setattr("builtins.input", mocked_input)

    openpipe.show.create_show(show_name)
