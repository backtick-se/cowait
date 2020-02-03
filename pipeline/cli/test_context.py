import os
import os.path
import pytest
from .const import CONTEXT_FILE_NAME
from .context import PipelineContext


def test_create_context():
    context = PipelineContext.open('test')
    assert context.path == os.path.join(os.getcwd(), 'test')
    assert context.path == context.root_path

    # raise error if path is invalid
    with pytest.raises(RuntimeError):
        context = PipelineContext.open('does_not_exist')

    # raise error if no context definition is found
    with pytest.raises(RuntimeError):
        PipelineContext.open()


def test_context_cwd():
    context = PipelineContext.open('test')

    # go to subdirectory
    subdir = context.cwd('subdir')
    assert subdir != context
    assert subdir.path != context.path

    # attempt to go to a directory that does not exist
    with pytest.raises(RuntimeError):
        context.cwd('does_not_exist')

    # attempt to go outside of context
    with pytest.raises(RuntimeError):
        context.cwd('..')


def test_get_values():
    context = PipelineContext.open('test')
    assert context['repo'] == 'repo'
    assert context['cluster.type'] == 'docker'

    # unset keys with a provided default should return the default
    assert context.get('cluster.undefined', 'nothing') == 'nothing'

    # uset parent with a provided default should return the default
    assert context.get('undefined.undefined', 'nothing') == 'nothing'

    # unset keys should raise errors
    with pytest.raises(KeyError):
        assert context.get('unset')

    # unset child keys with no default should raise errors
    with pytest.raises(KeyError):
        assert context['cluster.undefined']

    # unset child keys with unset parent no default should raise errors
    with pytest.raises(KeyError):
        assert context['undefined.undefined']


def test_get_files():
    context = PipelineContext.open('test')

    # context files
    path_abs = context.file('Dockerfile')
    path_rel = context.file_rel('Dockerfile')
    assert path_abs == os.path.join(context.path, 'Dockerfile')
    assert path_rel == 'Dockerfile'

    # return files in a subdirectory
    subdir = context.cwd('subdir')
    path_abs = subdir.file('Dockerfile')
    path_rel = subdir.file_rel('Dockerfile')
    assert path_abs == os.path.join(subdir.path, 'Dockerfile')
    assert path_rel == 'subdir/Dockerfile'

    # subdirectory should inherit files from the parent
    inherit_abs = subdir.file(CONTEXT_FILE_NAME)
    inherit_rel = subdir.file_rel(CONTEXT_FILE_NAME)
    assert inherit_abs == os.path.join(context.root_path, CONTEXT_FILE_NAME)
    assert inherit_rel == CONTEXT_FILE_NAME
