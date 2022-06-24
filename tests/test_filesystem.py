import os

import pytest
from pyfakefs.fake_filesystem_unittest import Patcher

from openpipe.filesystem import print_tree, PrintTreeOptions


@pytest.mark.smoke_test
@pytest.mark.parametrize("options", [
        pytest.param(None),
        pytest.param(PrintTreeOptions(show_dirs=False)),
        pytest.param(PrintTreeOptions(show_files=False)),
        pytest.param(PrintTreeOptions(show_symlinks=False)),
        pytest.param(PrintTreeOptions(show_hidden_files=False)),
        pytest.param(PrintTreeOptions(show_hidden_dirs=False)),
])
def test_print_tree_is_working(options):
    print_tree(".", options=options)


@pytest.mark.smoke_test
@pytest.mark.parametrize("options", [
        pytest.param(None),
        pytest.param(PrintTreeOptions(show_symlinks=True)),
        pytest.param(PrintTreeOptions(show_symlinks=False)),
])
def test_print_tree_against_symlink(options):
    with Patcher() as patcher:
        target_dir = '/some/path/to/check'

        source = os.path.join(target_dir, 'source')
        target = os.path.join(target_dir, 'target')

        patcher.fs.create_dir(target_dir)
        patcher.fs.create_file(target, contents="test")
        patcher.fs.create_symlink(source, target)

        #print("is %s a symlink?: %s" % (source, os.path.islink(source)))
        #print("is %s a symlink?: %s" % (target, os.path.islink(target)))

        print_tree(target_dir, options=options)
