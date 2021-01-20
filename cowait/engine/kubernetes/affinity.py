from kubernetes import client
from cowait.engine.const import LABEL_TASK_ID


affinity_schema = {
    'title': 'TaskAffinity',
    'type': 'object',

    'properties': {
        'mode': {
            'type': 'string',
            'enum': ['stack', 'spread'],
        },
        'required': {
            'type': 'bool',
        },
        'weight': {
            'type': 'number',
            'minimum': 0,
            'maximum': 100,
        },
        'label': {
            'type': 'string',
        },
        'namespaces': {
            'type': 'array',
            'items': {
                'type': 'string',
            },
        },
        'selectors': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'key': {
                        'type': 'string',
                    },
                    'operator': {
                        'type': 'string',
                        'enum': ['In', 'NotIn', 'Exists', 'DoesNotExist'],
                    },
                    'values': {
                        'type': 'array',
                        'items': {'type': 'string'},
                    },
                },
                'required': ['key', 'operator'],
            },
        },
    },
    'required': ['mode'],
}


def parse_affinity_item(affinity):
    return {
        'mode': affinity.get('mode', 'stack'),
        'required': affinity.get('required', False),
        'label': affinity.get('label', 'kubernetes.io/hostname'),
        'weight': affinity.get('weight', 1),
        'namespaces': affinity.get('namespaces', None),
        'selectors': affinity.get('selectors', [
            {'key': LABEL_TASK_ID, 'operator': 'Exists'},
        ]),
    }


def create_affinity_selector(selector):
    return client.V1LabelSelectorRequirement(
        key=selector.get('key'),
        operator=selector.get('operator'),
        values=selector.get('values', []),
    )


def create_affinity_term(item):
    return client.V1WeightedPodAffinityTerm(
        weight=item['weight'],
        pod_affinity_term=client.V1PodAffinityTerm(
            topology_key=item['label'],
            namespaces=item['namespaces'],
            label_selector=client.V1LabelSelector(
                match_expressions=[create_affinity_selector(s) for s in item['selectors']],
            ),
        )
    )


def create_affinity(affinity):
    affinities = []
    if affinity is None:
        return None
    elif isinstance(affinity, str):
        affinities = [{'mode': affinity}]
    elif isinstance(affinity, dict):
        affinities = [affinity]
    elif isinstance(affinity, list):
        pass
    else:
        raise ValueError('Illegal affinity definition')

    # fill with defaults
    affinities = [parse_affinity_item(item) for item in affinities]

    # sort into required/preferred, affinity/anti-affinity
    stack_req, stack_pref = [], []
    spread_req, spread_pref = [], []
    for item in affinities:
        term = create_affinity_term(item)
        if item['mode'] == 'stack':
            if item['required']:
                stack_req.append(term)
            else:
                stack_pref.append(term)
        elif item['mode'] == 'spread':
            if item['required']:
                spread_req.append(term)
            else:
                spread_pref.append(term)

    return client.V1Affinity(
        pod_affinity=client.V1PodAffinity(
            required_during_scheduling_ignored_during_execution=stack_req,
            preferred_during_scheduling_ignored_during_execution=stack_pref,
        ) if len(stack_req) + len(stack_pref) > 0 else None, 
        pod_anti_affinity=client.V1PodAntiAffinity(
            required_during_scheduling_ignored_during_execution=spread_req,
            preferred_during_scheduling_ignored_during_execution=spread_pref,
        ) if len(spread_req) + len(spread_pref) > 0 else None,
    )

