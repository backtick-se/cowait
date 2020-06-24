from .event_list import EventList


def test_push_output():
    output = EventList()
    output.append({'type': 'test'})
    output.append({'type': 'test'})
    assert len(output) == 2
    assert output.has(type='test')

    output.collect([{'type': 'one'}, {'type': 'two'}])
    assert output.has(type='one')
    assert output.has(type='two')


def test_output_matching():
    output = EventList()
    output.append({'type': 'test', 'field': 'hello team'})
    output.append({'type': 'other', 'field': 'hello team'})
    output.append({'type': 'test', 'field': 'wut'})
    output.append({'type': 'test'})
    assert output.count(type='test', field='tea.') == 1
    assert len(output.match(type='test', field='tea.')) == 1
