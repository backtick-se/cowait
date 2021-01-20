import pytest
from unittest.mock import Mock
from cowait.test import AsyncMock
from cowait.tasks.status import DONE, WORK
from cowait.tasks.messages import TASK_INIT, TASK_STATUS, TASK_FAIL, TASK_RETURN
from cowait.tasks.components import TaskManager
from cowait.utils import EventEmitter
from cowait.version import version


class MockTask(object):
    def __init__(self, id: str = '123'):
        self.id = id
        self.status = WORK
        self.node = Mock()
        self.cluster = Mock()
        self.taskdef = Mock()
        self.future = Mock()


def test_task_event_registration():
    task = MockTask()
    mgr = TaskManager(task)
    task.node.server.on.assert_any_call(TASK_INIT, mgr.on_child_init)
    task.node.server.on.assert_any_call(TASK_STATUS, mgr.on_child_status)
    task.node.server.on.assert_any_call(TASK_FAIL, mgr.on_child_fail)
    task.node.server.on.assert_any_call(TASK_RETURN, mgr.on_child_return)


async def test_task_message_forward():
    task = MockTask()
    task.node.server = EventEmitter()
    task.node.parent.send = AsyncMock()
    TaskManager(task)
    await task.node.server.emit('something', conn=AsyncMock())
    assert task.node.parent.send.called


async def test_task_watch_timeout():
    parent, child = MockTask(), MockTask()
    mgr = TaskManager(parent)
    mgr.emit_child_error = AsyncMock()
    child.wait_for_scheduling = AsyncMock()
    child.future.done = Mock(return_value=False)
    await mgr._init_timeout_check(child, 0)
    child.wait_for_scheduling.assert_called()
    parent.cluster.kill.assert_called_with(child.id)
    mgr.emit_child_error.assert_called()


async def test_task_watch_completed():
    parent, child = MockTask(), MockTask()
    mgr = TaskManager(parent)
    mgr.emit_child_error = AsyncMock()
    mgr.conns[child.id] = Mock()
    child.wait_for_scheduling = AsyncMock()
    child.future.done = Mock(return_value=True)
    await mgr._init_timeout_check(child, 0)
    child.wait_for_scheduling.assert_called()
    parent.cluster.kill.assert_not_called()
    mgr.emit_child_error.assert_not_called()


async def test_task_watch_ok():
    parent, child = MockTask(), MockTask()
    mgr = TaskManager(parent)
    mgr.conns[Mock()] = child.id # register connection
    mgr.emit_child_error = AsyncMock()
    child.wait_for_scheduling = AsyncMock()
    child.future.done = Mock(return_value=False)
    await mgr._init_timeout_check(child, 0)
    child.wait_for_scheduling.assert_called()
    parent.cluster.kill.assert_not_called()
    mgr.emit_child_error.assert_not_called()


async def test_version_check_reject():
    parent = MockTask()
    conn = Mock()
    mgr = TaskManager(parent)
    mgr.reject = AsyncMock()
    mgr.register = Mock()
    await mgr.on_child_init(conn, id='abc', task={}, version='invalid')
    mgr.reject.assert_called()
    mgr.register.assert_not_called()


async def test_version_check_accept():
    parent = MockTask()
    conn = Mock()
    mgr = TaskManager(parent)
    mgr.reject = AsyncMock()
    mgr.register = Mock()
    await mgr.on_child_init(conn, id='abc', task={}, version=version)
    mgr.reject.assert_not_called()
    mgr.register.assert_called()


async def test_task_register_watched():
    conn = Mock()
    parent, child = MockTask(), MockTask()
    mgr = TaskManager(parent)
    mgr[child.id] = child

    mgr.register(conn, child.id, {
        'id': str(child.id),
        'name': 'child',
        'image': 'test',
    })

    # connection should be stored
    assert conn in mgr.conns

    # task connection reference should be set
    assert mgr[child.id].conn == conn


async def test_task_register_virtual():
    conn = Mock()
    parent, child = MockTask(), MockTask()
    mgr = TaskManager(parent)

    assert child.id not in mgr

    mgr.register(conn, child.id, {
        'id': child.id,
        'name': 'child',
        'image': 'test',
        'parent': parent.id,
    })

    # connection should be stored
    assert conn in mgr.conns

    # a remote task instance should be created
    assert child.id in mgr
    assert mgr[child.id].conn == conn


async def test_child_disconnect():
    conn = Mock()
    parent, child = MockTask(), MockTask()
    mgr = TaskManager(parent)
    child.conn = conn
    child.status = DONE
    mgr.conns[conn] = child.id
    mgr[child.id] = child
    mgr.emit_child_error = AsyncMock()

    await mgr.on_child_close(conn)
    assert child.conn is None
    assert conn not in mgr.conns
    mgr.emit_child_error.assert_not_called()


async def test_child_lost():
    conn = Mock()
    parent, child = MockTask(), MockTask()
    mgr = TaskManager(parent)
    child.conn = conn
    mgr.conns[conn] = child.id
    mgr[child.id] = child
    mgr.emit_child_error = AsyncMock()

    await mgr.on_child_close(conn)
    assert child.conn is None
    assert conn not in mgr.conns
    mgr.emit_child_error.assert_called()

