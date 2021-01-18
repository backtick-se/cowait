from kubernetes import client
from cowait.engine.const import LABEL_TASK_ID


def create_ports(ports: dict) -> list:
    return [
        client.V1ContainerPort(**convert_port(port, host_port))
        for port, host_port in ports.items()
    ]


def convert_port(port, host_port: str = None):
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

