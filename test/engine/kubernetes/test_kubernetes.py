import pytest

import tempfile
from kubernetes import client

from cowait.engine.kubernetes.volumes import create_volumes
from cowait.engine.kubernetes import KubernetesProvider

EXAMPLE_KUBE_CONFIG = '''
current-context: test-context
apiVersion: v1
kind: Config

clusters:
- cluster:
    api-version: v1
    server: http://localhost:8080
  name: test-cluster

users:
- name: test-user
  user:
    token: test-token

contexts:
- context:
    cluster: test-cluster
    namespace: test-ns
    user: test-user
  name: test-context
'''


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


@pytest.mark.kubernetes
def test_provider__custom_kube_config():
    with tempfile.NamedTemporaryFile(mode='w+t') as kube_config_file:
        kube_config_file.write(EXAMPLE_KUBE_CONFIG)
        kube_config_file.seek(0)

        provider = KubernetesProvider(args={
            'context': 'test-context',
            'namespace': 'the-namespace',
            'kube_config_file': kube_config_file.name
        })

        assert provider.namespace == 'the-namespace'  # i.e. NOT 'test-ns' specified in the context
