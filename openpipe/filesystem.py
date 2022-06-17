"""
Snippets and functions to deal with the filesystem.
"""

import os


def print_tree(input_dir, max_level=3, current_level=1):
    """A cheap and dirty way to print a directory tree, similarly to how the
    unix tool 'tree' does it.

    :param input_dir: path to the directory to print
    :type input_dir: str

    :type level: int, optional
    """

    directories = sorted(os.listdir(input_dir))

    for entry in directories:

        prefix = "├"

        separator = "───" * current_level
        print(f"{prefix}{separator} {entry}")

        # Skip hidden files
        if entry.startswith("."):
            continue

        full_path = os.path.join(input_dir, entry)

        if os.path.isdir(full_path):
            if current_level == max_level:
                continue

            print_tree(full_path,
                       max_level=max_level,
                       current_level=current_level+1)

