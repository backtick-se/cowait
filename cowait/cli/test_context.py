import os
import os.path
import pytest
from .context import cowaitContext


def test_create_context():
    context = cowaitContext.open('test')
    assert context.root_path == os.path.join(os.getcwd(), 'test')

    # raise error if path is invalid
    with pytest.raises(ValueError):
        context = cowaitContext.open('does_not_exist')

    # raise error if no context definition is found
    local = cowaitContext.open()
    assert local.root_path == os.getcwd()


def test_get_values():
    context = cowaitContext.open('test')
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
    context = cowaitContext.open('test')

    # context files
    path_abs = context.file('Dockerfile')
    path_rel = context.file_rel('Dockerfile')
    assert path_abs == os.path.join(context.root_path, 'Dockerfile')
    assert path_rel == 'Dockerfile'
