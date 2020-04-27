import pytest
from asyncio import coroutine
from unittest.mock import Mock
from .emitter import EventEmitter


@pytest.mark.asyncio
async def test_emitter():
    emitter = EventEmitter()
    cb = Mock(side_effect=coroutine(Mock()))
    emitter.on('test', cb)
    await emitter.emit('test')
    cb.assert_called()


@pytest.mark.asyncio
async def test_emitter_wildcard():
    emitter = EventEmitter()
    cb = Mock(side_effect=coroutine(Mock()))
    emitter.on('*', cb)
    await emitter.emit('test')
    cb.assert_called()


@pytest.mark.asyncio
async def test_emitter_off():
    emitter = EventEmitter()
    cb = Mock(side_effect=coroutine(Mock()))
    emitter.on('test', cb)
    emitter.off('test', cb)
    await emitter.emit('test')
    cb.assert_not_called()
