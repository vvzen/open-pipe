import os
import re
import sys
import stat
import dataclasses
from collections import deque

import openpipe.logging
from openpipe.sanitization.core import name_for_filesystem
from openpipe.constant import SHOW_SCHEME_VERSION

log = openpipe.logging.get_logger('project.core')

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
SCHEMA_LINE_REGEX = re.compile(
    r"(?: )*(?P<name>\w+) (?P<permissions>\d{3}) *(?P<sticky>sticky)*")


@dataclasses.dataclass
class DirInfo:
    name: str
    permissions: int
    sticky: bool = False
    path: str = ""


def get_path_to_current_show_scheme():
    return os.path.join(CURRENT_DIR, "schema", SHOW_SCHEME_VERSION,
                        "showscheme.openpipe")


def parse_dir_tree_schema_line(line):
    """Parses a line of a 'show scheme' and returns the information that were
    retrieve as DirInfo instances

    :param line: line to parse
    :type line: str
    :return: the retrieved informations
    :rtype: DirInfo
    """

    match = SCHEMA_LINE_REGEX.match(line)
    if not match:
        return

    dict_result = match.groupdict()
    if not dict_result:
        return

    # Convert from the classic '755' notation expressed in octal
    # to its true integer equivalent
    permissions = int(dict_result["permissions"], base=8)
    dir_info = DirInfo(name=dict_result["name"], permissions=permissions)

    if dict_result.get("sticky"):
        dir_info.sticky = True

    return dir_info


def detect_indent(line, spaces_for_a_tab=4):
    count = 0
    for char in line:
        if char == " ":
            count += 1
        elif char == "\t":
            count += spaces_for_a_tab
        else:
            break
    return count


def read_directories_from_schema(schema_path):
    """Given a schema path, return a list of information that can be used
    to then create the directories on disk

    :param schema_path: abs path to schema
    :type schema_path: str
    :raises OSError: if the schema is not accessible on disk
    :return: information about the directories to create
    :rtype: list of DirInfo
    """

    if not os.path.exists(schema_path):
        log.error("Failed to read schema file from disk.")
        raise OSError("Cannot find '%s' on disk!" % schema_path)

    with open(schema_path, "r") as f:
        schema_data = f.read()

    # 1. Parse the schema file
    dirs_to_create = []
    current_indent = 0
    current_path = deque()

    # Skip first line since it contains only the 'root' keyword
    lines = schema_data.split("\n")[1:]

    for index, line in enumerate(lines):
        dir_info = parse_dir_tree_schema_line(line)
        if not dir_info:
            continue

        indent = detect_indent(line)

        if index == 0:
            current_path.append(dir_info.name)

        elif indent == current_indent:
            current_path.pop()
            current_path.append(dir_info.name)

        elif indent > current_indent:
            current_path.append(dir_info.name)

        elif indent < current_indent:
            delta = abs((indent - current_indent) // 4)
            current_path.pop()
            for _ in range(delta):
                current_path.pop()
            current_path.append(dir_info.name)

        dir_info.path = "/".join(current_path)
        dirs_to_create.append(dir_info)
        current_indent = indent

    return dirs_to_create


def create_project(project_name, root_path):
    """Creates a project on disk using a certain schema tree

    :param project_name: name of the project
    :type project_name: str
    """

    safe_project_name = name_for_filesystem(project_name)

    if safe_project_name != project_name:
        log.info("Project name was automatically converted from %s to %s",
                 project_name, safe_project_name)
        reply = input("Is that ok? y/n:  ")
        if reply.lower() not in ["y", "yes"]:
            log.info("User did not agree with project name change. Exiting..")
            sys.exit(1)

    # Gather schema
    schema_path = get_path_to_current_show_scheme()
    log.info("Reading schema from %s", schema_path)

    dirs_to_create = read_directories_from_schema(schema_path)
    log.info("Started creation of directories on disk..")

    if not os.path.exists(os.path.dirname(root_path)):
        raise OSError("Root path doesn't exist on disk: %s" % root_path)

    # Create with open permissions..
    project_root_path = os.path.join(root_path, safe_project_name)
    os.mkdir(project_root_path, mode=0o777)

    for dir_info in dirs_to_create:
        current_path = os.path.join(project_root_path, dir_info.path)
        os.mkdir(current_path)
        os.chmod(current_path, 0o777)

    # ..and then lock down everything
    for dir_info in dirs_to_create[::-1]:
        current_path = os.path.join(project_root_path, dir_info.path)
        if dir_info.sticky:
            os.chmod(current_path, mode=dir_info.permissions | stat.S_ISVTX)
        else:
            if dir_info.permissions == 0o777:
                continue
            os.chmod(current_path, mode=dir_info.permissions)

    os.chmod(project_root_path, mode=0o755)
    log.info("Done!")
