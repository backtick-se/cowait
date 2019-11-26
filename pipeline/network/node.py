from typing import Any
from pipeline.tasks.status import WAIT, WORK, DONE, STOP, FAIL
from .push import PushSocket
from .pull import PullSocket

import json
import asyncio
import websockets

import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

class Client:
    def __init__(self, target):
        self.target = target

    async def connect(self):
        self.ws = await websockets.connect(self.target)

    async def send(self, msg):
        await self.ws.send(json.dumps(msg))

class Server:
    def __init__(self, port):
        self.port = port

    async def serve(self, handler):
        async def connection(ws, path):
            print('ws connection')
            while True:
                msg = await ws.recv()
                print('recv', msg)
                handler(json.loads(msg))

        await websockets.serve(connection, "0.0.0.0", self.port)
        while True:
            await asyncio.sleep(1)


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


    def handle(self, msg) -> None:
        for handler in self.handlers:
            handler.handle(**msg)


    async def send(self, msg: dict) -> None:
        if isinstance(msg, list):
            for m in msg:
                await self.send(m)
        else:
            if not 'id' in msg:
                msg['id'] = self.id
            if self.upstream:
                await self.upstream.send(msg)
            self.handle(msg)

    
    def attach(self, handler: callable) -> None:
        self.handlers.append(handler)


    def detach(self, handler: callable) -> None:
        self.handlers.remove(handler)

    #
    # protocol client:
    # put it somewhere else
    #

    async def send_msg(self, type: str, **msg):
        """
        Send a message upstream.

        Arguments:
            type (str): Message type
            kwargs (dict): Message fields
        """
        await self.send({
            'id': self.id,
            'type': type,
            **msg,
        })

    
    async def send_init(self, taskdef) -> None:
        """
        Send a task initialization message.

        Arguments:
            taskdef (TaskDefinition): New task definition
        """
        await self.send_msg('init', task=taskdef.serialize())


    async def send_run(self) -> None:
        """ Send status update: Running """
        await self.send_msg('status', status=WORK)


    async def send_stop(self, id=None) -> None:
        """ Send status update: Stopped """
        await self.send_msg('status', status=STOP, id=id)
        await self.send_msg('return', result={}, id=id)


    async def send_done(self, result: Any) -> None:
        """ 
        Send status update: Done, and return a result.

        Arguments:
            result (any): Any json-serializable data to return to the upstream task.
        """
        await self.send_msg('status', status=DONE)
        await self.send_msg('return', result=result)


    async def send_fail(self, error: str) -> None:
        """
        Send an error.

        Arguments:
            error (str): Error message
        """
        await self.send_msg('status', status=FAIL)
        await self.send_msg('fail',   error=error)


    async def send_log(self, file: str, data: str) -> None:
        """
        Send captured log output.

        Arguments:
            file (str): Capture source (stdout/stderr)
            data (str): Captured output data
        """
        await self.send_msg('log', file=file, data=data)