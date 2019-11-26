import json
import asyncio
import websockets


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
