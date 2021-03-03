import pytest
from unittest.mock import patch
from kubernetes import client
from cowait.engine.kubernetes.utils import _parse_env, _parse_env_from


@patch('cowait.engine.kubernetes.utils._parse_env_from')
def test_parse_env(_parse_env_from):
    env = _parse_env('str', 'value')
    assert isinstance(env, client.V1EnvVar)
    assert not _parse_env_from.called
    assert env.name == 'str'
    assert env.value == 'value'


def test_parse_env_int():
    env = _parse_env('str', 1)
    assert env.value == '1'


@patch('cowait.engine.kubernetes.utils._parse_env_from')
def test_parse_env_from(_parse_env_from):
    env = _parse_env('dict', {})
    assert isinstance(env, client.V1EnvVar)
    assert _parse_env_from.called
    assert env.name == 'dict'
    assert env.value_from == _parse_env_from.return_value


def test_parse_env_from_secret():
    env = {
        'source': 'secret',
        'name': 'name',
        'key': 'key',
    }
    value = _parse_env_from(env)
    assert isinstance(value, client.V1EnvVarSource)

    ref = value.secret_key_ref
    assert isinstance(ref, client.V1SecretKeySelector)
    assert ref.name == env['name']
    assert ref.key == env['key']

    with pytest.raises(KeyError):
        _parse_env_from({'source': 'secret'})

    with pytest.raises(KeyError):
        _parse_env_from({'source': 'secret', 'name': 'name'})

    with pytest.raises(KeyError):
        _parse_env_from({'source': 'secret', 'key': 'key'})


def test_parse_env_from_configmap():
    env = {
        'source': 'configmap',
        'name': 'name',
        'key': 'key',
    }
    value = _parse_env_from(env)
    assert isinstance(value, client.V1EnvVarSource)

    ref = value.config_map_key_ref
    assert isinstance(ref, client.V1ConfigMapKeySelector)
    assert ref.name == env['name']
    assert ref.key == env['key']

    with pytest.raises(KeyError):
        _parse_env_from({'source': 'configmap'})

    with pytest.raises(KeyError):
        _parse_env_from({'source': 'configmap', 'name': 'name'})

    with pytest.raises(KeyError):
        _parse_env_from({'source': 'configmap', 'key': 'key'})


def test_parse_env_from_invalid():
    with pytest.raises(ValueError):
        _parse_env_from({'source': 'wut'})

    with pytest.raises(ValueError):
        _parse_env_from({})
