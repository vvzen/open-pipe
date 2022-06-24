"""
Snippets and functions to deal with the filesystem.
"""

import os


class PrintTreeOptions(object):

    def __init__(self):
        self.show_dirs = True
        self.show_files = True
        self.show_symlinks = True
        self.show_hidden_files = False
        self.show_hidden_dirs = False


def print_tree(input_dir, options=None, max_level=3,
               _current_level=1, _num_files=0, _num_dirs=0):
    """A cheap and dirty way to print a directory tree, similarly to how the
    unix tool 'tree' does it, but dumbed down (for now).

    :param input_dir: path to the directory to print
    :type input_dir: str

    :param level: how many levels to print
    :type level: int, optional

    :param _current_level: ignore it. It's used by the implementation only and
        should not be used by the caller.
    :type current_level: int, optional

    :param _num_files: ignore it. It's used by the implementation only and
        should not be used by the caller.
    :type _num_files: int, optional

    :param _num_dirs: ignore it. It's used by the implementation only and
        should not be used by the caller.
    :type _num_dirs: int, optional
    """

    if not options:
        options = PrintTreeOptions()

    entries = os.listdir(input_dir)

    directories = sorted([
        d for d in entries
        if os.path.isdir(os.path.join(input_dir, d))
    ])
    files = sorted([
        f for f in entries
        if os.path.isfile(os.path.join(input_dir, f))
    ])

    if options.show_files:
        for index, file in enumerate(files):
            is_first_entry = index == 0
            is_last_entry = index == len(files) - 1

            is_symlink = os.path.islink(os.path.join(input_dir, file))

            if not options.show_symlinks and is_symlink:
                continue

            prefix = "├"
            if is_last_entry:
                prefix = "└"
            elif is_first_entry:
                prefix = "├"

            separator = "  " * _current_level
            print(f"{separator} {prefix} {file}")

            _num_files += 1

            if not options.show_hidden_files and file.startswith("."):
                continue

    if options.show_dirs:
        for index, directory in enumerate(directories):

            prefix = "*"

            separator = "  " * _current_level
            print(f"{separator} {prefix} {directory}")

            if not options.show_hidden_dirs and directory.startswith("."):
                continue

            _num_dirs += 1

            if _current_level == max_level:
                continue

            print_tree(os.path.join(input_dir, directory),
                       options=options,
                       max_level=max_level,
                       _current_level=_current_level+1,
                       _num_files=_num_files,
                       _num_dirs=_num_dirs)

    # Exit condition
    if _current_level == 1:
        print(f"\n{_num_dirs} directories, {_num_files} files")
