from typing import List
from kubernetes.client import V1EnvVar, V1EnvVarSource, V1SecretKeySelector, \
    V1ConfigMapKeySelector, V1ContainerPort
from cowait.tasks import TaskDefinition
from cowait.engine.utils import base_environment


def create_env(cluster, taskdef: TaskDefinition) -> List[V1EnvVar]:
    """Creates a kubernetes environment configuration"""
    env = base_environment(cluster, taskdef)
    return [
        _parse_env(key, value)
        for key, value in env.items()
    ]


def _parse_env(name: str, value) -> V1EnvVar:
    """Parses an environment value into a kubernetes EnvVar"""
    if isinstance(value, dict):
        return V1EnvVar(
            name=str(name),
            value_from=_parse_env_from(value),
        )
    return V1EnvVar(name=str(name), value=str(value))


def _parse_env_from(value_from: dict) -> V1EnvVarSource:
    """Parses an environment value dict into an EnvVarSource"""
    source = value_from.get('source', '').lower()
    if source == 'secret':
        return V1EnvVarSource(
            secret_key_ref=V1SecretKeySelector(
                name=value_from['name'],
                key=value_from['key'],
            ),
        )
    elif source == 'configmap':
        return V1EnvVarSource(
            config_map_key_ref=V1ConfigMapKeySelector(
                name=value_from['name'],
                key=value_from['key'],
            ),
        )
    else:
        raise ValueError(f'Unsupported environment source "{source}"')


def create_ports(ports: dict) -> List[V1ContainerPort]:
    return [
        V1ContainerPort(**_parse_port(port, host_port))
        for port, host_port in ports.items()
    ]


def _parse_port(port, host_port: str = None) -> dict:
    protocol = 'TCP'
    if isinstance(port, str) and '/' in port:
        slash = port.find('/')
        protocol = port[slash+1:]
        port = port[:slash]

    if host_port is None:
        host_port = port

    return {
        'protocol': protocol.upper(),
        'container_port': int(port),
        'host_port': int(host_port),
    }
