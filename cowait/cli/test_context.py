import os
import os.path
import pytest
from .context import CowaitContext


def test_create_context():
    context = CowaitContext.open('test')
    assert context.root_path == os.path.join(os.getcwd(), 'test')

    # raise error if path is invalid
    with pytest.raises(ValueError):
        context = CowaitContext.open('does_not_exist')

    # raise error if no context definition is found
    local = CowaitContext.open()
    assert local.root_path == os.getcwd()


def test_get_files():
    context = CowaitContext.open('test')

    # context files
    path_abs = context.file('Dockerfile')
    path_rel = context.file_rel('Dockerfile')
    assert path_abs == os.path.join(context.root_path, context.get('workdir', '.'), 'Dockerfile')
    assert path_rel == 'Dockerfile'
