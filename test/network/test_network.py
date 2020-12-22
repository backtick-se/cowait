import asyncio
from cowait.network.errors import AuthError
import pytest
from cowait.test import AsyncMock
from cowait.network.server import Server
from cowait.network.client import Client
from cowait.network.const import PORT, ON_CONNECT, ON_CLOSE, ON_ERROR, WS_PATH


@pytest.mark.network
async def test_network():
    token = 'hello_team'

    # client setup
    client = Client()
    on_client_greeting = client.on('greeting', AsyncMock())
    on_client_connect = client.on(ON_CONNECT, AsyncMock())
    on_client_close = client.on(ON_CLOSE, AsyncMock())

    # server setup
    server = Server(port=PORT)
    server.auth.add_token(token)

    on_server_connect = server.on(ON_CONNECT, AsyncMock())
    on_server_close = server.on(ON_CLOSE, AsyncMock())
    on_server_error = server.on(ON_ERROR, AsyncMock())
    on_server_greeting = server.on('greeting', AsyncMock())

    # server should send a greeting to the client upon connection
    async def send_greeting(conn):
        await conn.send({'type': 'greeting', 'message': 'hello client'})
    server.on(ON_CONNECT, send_greeting)

    # actual test code
    asyncio.create_task(server.serve())
    asyncio.create_task(client._connect(f'ws://localhost:{PORT}/{WS_PATH}', token))

    for _ in range(10):
        await asyncio.sleep(0.1)
        if client.connected:
            break

    await client.send({'type': 'greeting', 'message': 'hello server'})
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


@pytest.mark.network
async def test_network_authentication():
    client = Client()
    server = Server(port=PORT)

    asyncio.create_task(server.serve())

    with pytest.raises(AuthError):
        await client.connect(f'ws://localhost:{PORT}/{WS_PATH}', '')

    await server.close()
