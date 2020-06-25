from .event_log import EventLog


def test_push_output():
    output = EventLog()
    output.append({'type': 'test'})
    output.append({'type': 'test'})
    assert len(output) == 2
    assert output.has(type='test')

    output.collect([{'type': 'one'}, {'type': 'two'}])
    assert output.has(type='one')
    assert output.has(type='two')


def test_output_matching():
    output = EventLog()
    output.append({'type': 'test', 'field': 'hello team'})
    output.append({'type': 'other', 'field': 'hello team'})
    output.append({'type': 'test', 'field': 'wut'})
    output.append({'type': 'test'})
    assert output.count(type='test', field='tea.') == 1
    assert output.count(field='tea.') == 2
    assert len(output.match(type='test', field='tea.')) == 1
