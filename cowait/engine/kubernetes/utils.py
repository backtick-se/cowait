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


def create_affinity(affinity: str):
    if affinity not in [None, 'stack', 'spread']:
        raise ValueError(f'Unknown affinity mode `{affinity}`')

    affinity_term = client.V1WeightedPodAffinityTerm(
        weight=100,
        pod_affinity_term=client.V1PodAffinityTerm(
            topology_key='kubernetes.io/hostname',
            label_selector=client.V1LabelSelector(
                match_expressions=[
                    client.V1LabelSelectorRequirement(
                        key=LABEL_TASK_ID,
                        operator='Exists',
                    ),
                ]
            )
        )
    )
    return client.V1Affinity(
        pod_affinity=client.V1PodAntiAffinity(
            preferred_during_scheduling_ignored_during_execution=[affinity_term]
        ) if affinity == 'stack' else None,

        pod_anti_affinity=client.V1PodAntiAffinity(
            preferred_during_scheduling_ignored_during_execution=[affinity_term]
        ) if affinity == 'spread' else None,
    )

