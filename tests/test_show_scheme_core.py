import os

import pytest

from openpipe.show_scheme.core import (DirInfo, parse_dir_tree_schema_line,
                                       detect_indent, create_project,
                                       read_directories_from_schema,
                                       get_path_to_current_show_scheme)

from conftest import SAMPLES_DIR

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


def test_read_directories_from_schema_missing_schema():
    with pytest.raises(OSError):
        read_directories_from_schema("/a/missing/path")

# Smoke tests
# -----------------------------------------------------------------------------
# Only check that things are still working in order to prevent
# potential regressions
def test_read_directories_from_schema():
    current_schema_path = get_path_to_current_show_scheme()
    read_directories_from_schema(current_schema_path)

@pytest.mark.parametrize("schema_path", [
    pytest.param(os.path.join(SAMPLES_DIR, "schemas", "schema_with_wrong_indentation.openpipe"))
])
def test_read_directories_from_schema_wrong_schemas(schema_path):
    with pytest.raises(ValueError):
        read_directories_from_schema(schema_path)


@pytest.mark.parametrize("project_name, is_missing_root_path", [
    pytest.param("something", False),
    pytest.param("Some Name", True),
])
def test_create_project(monkeypatch, fs,
                        project_name, is_missing_root_path):

    current_schema_path = get_path_to_current_show_scheme()
    fs.add_real_file(current_schema_path)

    # Create a fake directory
    root_path = "/tmp/my/root"
    if not is_missing_root_path:
        fs.create_dir(root_path)

    # Mock the reply from the user
    monkeypatch.setattr("builtins.input", lambda prompt="": "y")

    if is_missing_root_path:
        with pytest.raises(OSError):
            create_project(project_name, root_path)
    else:
        create_project(project_name, root_path)
