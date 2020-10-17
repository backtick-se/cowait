import asyncio
import pytest
from cowait.test import AsyncMock
from .server import Server
from .client import Client


@pytest.mark.network
@pytest.mark.async_timeout(20)
async def test_network():
    port = 12389
    token = 'hello team'

    # client setup
    client = Client()
    on_client_greeting = client.on('greeting', AsyncMock())
    on_client_connect = client.on('__connect', AsyncMock())
    on_client_close = client.on('__close', AsyncMock())

    # server setup
    server = Server(port=port)
    server.auth.add_token(token)

    on_server_connect = server.on('__connect', AsyncMock())
    on_server_close = server.on('__close', AsyncMock())
    on_server_error = server.on('__error', AsyncMock())
    on_server_greeting = server.on('greeting', AsyncMock())

    # server should send a greeting to the client upon connection
    async def send_greeting(conn):
        await conn.send({'type': 'greeting', 'message': 'hello client'})
    server.on('__connect', send_greeting)

    # actual test code
    asyncio.create_task(server.serve())
    asyncio.create_task(client._connect(f'ws://localhost:{port}/ws', token))

    for _ in range(10):
        await asyncio.sleep(0.1)
        if client.connected:
            break

    await client.send({ 'type': 'greeting', 'message': 'hello server' })
    await client.close()
    await server.close()

    # check server events
    assert not on_server_error.called
    assert on_server_greeting.called
    assert on_server_greeting.call_args[1]['message'] == 'hello server'
    assert on_server_connect.called
    assert on_server_close.called

    # check client events
    assert on_client_greeting.called
    assert on_client_greeting.call_args[1]['message'] == 'hello client'
    assert on_client_greeting.called
    assert on_client_connect.called
    assert on_client_close.called
