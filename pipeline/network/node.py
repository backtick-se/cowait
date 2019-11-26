from typing import Any
from pipeline.tasks.status import WAIT, WORK, DONE, STOP, FAIL
from .push import PushSocket
from .pull import PullSocket

import json
import asyncio
import websockets

class Client:
    def __init__(self, target):
        self.target = target

    async def connect(self):
        self.ws = await websockets.connect(self.target)

    async def send(self, msg):
        await self.ws.send(json.dumps(msg))
    
    async def close(self):
        return await self.ws.close()


class Server:
    def __init__(self, port):
        self.port = port
        self.running = False

    async def serve(self, handler):
        async def connection(ws, path):
            while ws.connected:
                msg = await ws.recv()
                handler(json.loads(msg))

        self.running = True
        self.ws = await websockets.serve(connection, "0.0.0.0", self.port)
        while self.running:
            await asyncio.sleep(0.1)

    def close(self):
        self.ws.close()
        self.running = False


class Node(object):
    def __init__(self, id):
        self.id = id
        self.upstream = None
        self.daemon = None
        self.handlers = [ ]


    async def connect(self, target):
        self.upstream = Client(target)
        await self.upstream.connect()


    def bind(self, bind):
        self.daemon = Server(bind)


    async def serve(self):
        await self.daemon.serve(self.handle)


    async def close(self):
        if self.daemon:
            self.daemon.close()
        if self.upstream:
            await self.upstream.close()


    def handle(self, msg) -> None:
        for handler in self.handlers:
            handler.handle(**msg)


    def send(self, msg: dict) -> None:
        if isinstance(msg, list):
            for m in msg:
                self.send(m)
        else:
            if not 'id' in msg:
                msg['id'] = self.id
            if self.upstream:
                asyncio.ensure_future(self.upstream.send(msg))
            self.handle(msg)

    
    def attach(self, handler: callable) -> None:
        self.handlers.append(handler)


    def detach(self, handler: callable) -> None:
        self.handlers.remove(handler)

    #
    # protocol client:
    # put it somewhere else
    #

    def send_msg(self, type: str, **msg):
        """
        Send a message upstream.

        Arguments:
            type (str): Message type
            kwargs (dict): Message fields
        """
        self.send({
            'id': self.id,
            'type': type,
            **msg,
        })

    
    def send_init(self, taskdef) -> None:
        """
        Send a task initialization message.

        Arguments:
            taskdef (TaskDefinition): New task definition
        """
        self.send_msg('init', task=taskdef.serialize())


    def send_run(self) -> None:
        """ Send status update: Running """
        self.send_msg('status', status=WORK)


    def send_stop(self, id=None) -> None:
        """ Send status update: Stopped """
        self.send_msg('status', status=STOP, id=id)
        self.send_msg('return', result={}, id=id)


    def send_done(self, result: Any) -> None:
        """ 
        Send status update: Done, and return a result.

        Arguments:
            result (any): Any json-serializable data to return to the upstream task.
        """
        self.send_msg('status', status=DONE)
        self.send_msg('return', result=result)


    def send_fail(self, error: str) -> None:
        """
        Send an error.

        Arguments:
            error (str): Error message
        """
        self.send_msg('status', status=FAIL)
        self.send_msg('fail',   error=error)


    def send_log(self, file: str, data: str) -> None:
        """
        Send captured log output.

        Arguments:
            file (str): Capture source (stdout/stderr)
            data (str): Captured output data
        """
        self.send_msg('log', file=file, data=data)