from kubernetes import client
from cowait.engine.const import LABEL_TASK_ID
from cowait.engine.kubernetes.affinity import create_affinity


def test_create_str_stack_affinity():
    affinity = create_affinity('stack')
    assert isinstance(affinity, client.V1Affinity)
    assert affinity.pod_anti_affinity is None
    item = affinity.pod_affinity.preferred_during_scheduling_ignored_during_execution[0]
    assert len(affinity.pod_affinity.required_during_scheduling_ignored_during_execution) == 0
    assert item.weight == 1
    term = item.pod_affinity_term
    assert term.namespaces is None
    assert term.topology_key == 'kubernetes.io/hostname'
    expr = term.label_selector.match_expressions[0] 
    assert expr.key == LABEL_TASK_ID
    assert expr.operator == 'Exists'
    assert expr.values == []


def test_create_str_spread_affinity():
    affinity = create_affinity('spread')
    assert isinstance(affinity, client.V1Affinity)
    assert affinity.pod_affinity is None
    item = affinity.pod_anti_affinity.preferred_during_scheduling_ignored_during_execution[0]
    assert len(affinity.pod_anti_affinity.required_during_scheduling_ignored_during_execution) == 0
    assert item.weight == 1
    term = item.pod_affinity_term
    assert term.namespaces is None
    assert term.topology_key == 'kubernetes.io/hostname'
    expr = term.label_selector.match_expressions[0] 
    assert expr.key == LABEL_TASK_ID
    assert expr.operator == 'Exists'
    assert expr.values == []


def test_create_dict_affinity():
    affinity = create_affinity({
        'mode': 'stack',
        'required': True,
        'namespaces': ['default'],
        'label': 'topology_key',
        'weight': 90,
        'selectors': [
            {'key': 'task', 'operator': 'In', 'values': ['a', 'b']},
        ],
    })

    assert isinstance(affinity, client.V1Affinity)
    assert affinity.pod_anti_affinity is None
    assert len(affinity.pod_affinity.preferred_during_scheduling_ignored_during_execution) == 0
    item = affinity.pod_affinity.required_during_scheduling_ignored_during_execution[0]
    assert item.weight == 90
    term = item.pod_affinity_term
    assert term.namespaces == ['default']
    assert term.topology_key == 'topology_key'
    expr = term.label_selector.match_expressions[0] 
    assert expr.key == 'task'
    assert expr.operator == 'In'
    assert expr.values == ['a', 'b']

