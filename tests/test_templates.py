import pytest

from openpipe.templates import render_template


@pytest.mark.behaviour_test
@pytest.mark.parametrize("show_name,template_name,fields,expected_string", [
    # 0. The vanilla template
    pytest.param(
        "test_show",
        "default_workfile",
        {
            "context_path": "sc010/sc010_0010",
            "context_name": "sc010_0010",
            "stream": "default",
            "task": "my-task",
            "version": "003",
        },
        "test_show/sc010/sc010_0010/work/sc010_0010_my-task_default_v003"
    ),
    # 1. A Houdini scene
    pytest.param(
        "test_show",
        "houdini_workfile",
        {
            "context_path": "sc010/sc010_0010",
            "context_name": "sc010_0010",
            "stream": "default",
            "task": "fx",
            "version": "010",
        },
        "test_show/sc010/sc010_0010/work/sc010_0010_fx_default_v010.hip"
    ),
    # 2. A Nuke script
    pytest.param(
        "test_show",
        "nuke_workfile",
        {
            "context_path": "sc030/sc030_0010",
            "context_name": "sc030_0010",
            "stream": "default",
            "task": "comp",
            "version": "014",
        },
        "test_show/sc030/sc030_0010/work/sc030_0010_comp_default_v014.nk"
    )
])
def test_render_template(monkeypatch, show_name,
                         template_name, fields, expected_string):

    monkeypatch.setenv("OPENPIPE_SHOW", show_name)

    assert render_template(template_name, fields) == expected_string
