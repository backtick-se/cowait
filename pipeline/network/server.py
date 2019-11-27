import json
import asyncio
import websockets
from .conn import Conn

ANY_IP = '0.0.0.0'


class Server:
    def __init__(self, port: int):
        self.port = port
        self.conns = [ ]


    async def serve(self, handler: callable):
        # serve websockets
        self.ws = await websockets.serve(
            lambda ws, path: self.on_client(ws, handler),
            host=ANY_IP, 
            port=self.port,
        )

        # wait forever.
        while True:
            await asyncio.sleep(1)


    async def on_client(self, ws, handler):
        conn = Conn(ws)
        self.conns.append(conn)

        try:
            while True:
                msg = await conn.recv()
                await handler(conn, msg)

        except websockets.exceptions.ConnectionClosedOK:
            print('ws client disconnected')

        finally:
            self.conns.remove(conn)


    async def send(self, msg: dict):
        try:
            js = json.dumps(msg)
            for conn in self.conns:
                await conn.ws.send(js)
        except websockets.exceptions.ConnectionClosedOK:
            return None


    def close(self):
        self.ws.close()
