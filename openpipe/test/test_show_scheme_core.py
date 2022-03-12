import pytest

from openpipe.show_scheme.core import (DirInfo, parse_dir_tree_schema_line,
                                       detect_indent, create_project,
                                       read_directories_from_schema,
                                       get_path_to_current_show_scheme)

@pytest.mark.parametrize("input_line,output", [
    pytest.param("asset 755", DirInfo(name="asset", permissions=0o755, sticky=False)),
    pytest.param("    pipeline 775", DirInfo(name="pipeline", permissions=0o775, sticky=False)),
    pytest.param("tmp 777 sticky", DirInfo(name="tmp", permissions=0o777, sticky=True)),
])
def test_parse_dir_tree_schema_line(input_line, output):
    assert parse_dir_tree_schema_line(input_line) == output


@pytest.mark.parametrize("input_line,indent_num", [
    pytest.param("    asset 755", 4),
    pytest.param("        pipeline 775", 8),
    pytest.param("\tsomething", 4),
    pytest.param("\t\ttmp 777 sticky", 8)
])
def test_detect_indent(input_line,indent_num):
    assert detect_indent(input_line) == indent_num


# Smoke tests
# -----------------------------------------------------------------------------
# Only check that things are still working in order to prevent
# potential regressions
def test_read_directories_from_schema():
    current_schema_path = get_path_to_current_show_scheme()
    read_directories_from_schema(current_schema_path)

@pytest.mark.parametrize("project_name", [
    pytest.param("something"),
    pytest.param("Some Name"),
])
def test_create_project(monkeypatch, fs, project_name):
    # Add a real file to the fake filesystem
    # See http://jmcgeheeiv.github.io/pyfakefs/master/usage.html#access-to-files-in-the-real-file-system
    current_schema_path = get_path_to_current_show_scheme()
    fs.add_real_file(current_schema_path)

    # Create a fake directory
    root_path = "/tmp/my/root"
    fs.create_dir(root_path)

    # Mock the reply from the user
    monkeypatch.setattr("builtins.input", lambda prompt="": "y")
    create_project(project_name, root_path)
