import pytest
from cowait.tasks.graph import Graph, Node, Result


@pytest.mark.task_graph
def test_node_dependencies():
    g = Graph()
    b = g.node('B')
    g.node('A', {
        'b': b,
        'number': 123,
    })

    # expect B to be returned first
    first = g.next()
    assert first is not None
    assert first.task == 'B'
    assert first.inputs == {}

    # at this point, no new node should be available until b is completed
    assert g.next() is None

    g.complete(b, 'yey')

    # finally, A should be returned with the output of B as input
    second = g.next()
    assert second is not None
    assert second.task == 'A'
    assert second.inputs == {'b': 'yey', 'number': 123}


@pytest.mark.task_graph
def test_node_upstream_error():
    g = Graph()
    b = g.node('B')
    a = g.node('A', {
        'b': b,
    })

    g.fail(b, Exception('test'))
    assert b in g.errors
    assert a not in g.errors

    # node of the nodes should be ready
    # A should be marked as failed
    assert g.next() is None

    assert a in g.errors


@pytest.mark.task_graph
def test_node_output_accessor():
    g = Graph()
    b = g.node('B')
    g.node('A', inputs={
        'one': b.output('value'),
        'two': b.output(lambda x: x['value'] * 2),
    })
    g.complete(b, {'value': 2})

    result = g.next()
    assert result is not None
    assert result.inputs['one'] == 2
    assert result.inputs['two'] == 4


@pytest.mark.task_graph
def test_unpack_result():
    outputs = {'a': 123}

    r1 = Result(None, 'a')
    assert r1.get(outputs) == 123

    r2 = Result(None, lambda x: x['a'] * 2)
    assert r2.get(outputs) == 246


@pytest.mark.task_graph
def test_graph_node_ids():
    a = Node.next_id()
    b = Node.next_id()
    assert b > a
