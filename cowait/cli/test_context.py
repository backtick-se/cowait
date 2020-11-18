import os
import os.path
import pytest
from .context import Context


def test_create_context():
    context = Context.open(None, 'test')
    assert context.root_path == os.path.join(os.getcwd(), 'test')

    # raise error if path is invalid
    with pytest.raises(ValueError):
        context = Context.open(None, 'does_not_exist')

    # create empty context in current directory if no definition is found
    local = Context.open(None)
    assert local.root_path == os.getcwd()


def test_get_files():
    context = Context.open(None, 'test')

    # context files
    path_abs = context.file('Dockerfile')
    path_rel = context.file_rel('Dockerfile')
    assert path_abs == os.path.join(context.root_path, context.get('workdir', '.'), 'Dockerfile')
    assert path_rel == 'Dockerfile'
