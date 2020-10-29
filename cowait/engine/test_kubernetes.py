import pytest
from kubernetes import client
from .kubernetes import create_volumes


@pytest.mark.kubernetes
def test_create_volumes():
    target_path = '/target/path'
    source_path = '/source/path'

    volumes, mounts = create_volumes({
        target_path: {
            'read_only': True,
            'host_path': {
                'path': source_path,
            },
        },
    })

    assert len(volumes) == 1
    assert len(mounts) == 1

    volume = volumes[0]
    assert isinstance(volume, client.V1Volume)
    assert isinstance(volume.host_path, client.V1HostPathVolumeSource)
    assert volume.host_path.path == source_path

    mount = mounts[0]
    assert isinstance(mount, client.V1VolumeMount)
    assert mount.name == 'volume1'
    assert mount.mount_path == target_path
    assert mount.read_only
