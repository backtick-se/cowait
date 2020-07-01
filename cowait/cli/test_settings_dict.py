import pytest
from .settings_dict import SettingsDict


def test_get_values():
    settings = SettingsDict(data={
        'repo': 'repo',
        'cluster': {
            'type': 'docker',
        },
    })
    assert settings['repo'] == 'repo'
    assert settings['cluster.type'] == 'docker'

    # unset keys with a provided default should return the default
    assert settings.get('cluster.undefined', 'nothing') == 'nothing'

    # uset parent with a provided default should return the default
    assert settings.get('undefined.undefined', 'nothing') == 'nothing'

    assert settings.has('repo')
    assert settings.has('cluster.type')

    # unset keys without a default should raise errors
    with pytest.raises(KeyError):
        assert settings.get('unset')

    # unset child keys with no default should raise errors
    with pytest.raises(KeyError):
        assert settings['cluster.undefined']

    # unset child keys with unset parent no default should raise errors
    with pytest.raises(KeyError):
        assert settings['undefined.undefined']


def test_set_values():
    settings = SettingsDict(data={})
    settings['nested.key'] = 1
    assert isinstance(settings.data['nested'], dict)
    assert settings.data['nested']['key'] == 1

    settings['nested.key2'] = 2
    assert settings.data['nested'] == {'key': 1, 'key2': 2}
