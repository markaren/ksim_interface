
import json
import asyncio
import websockets

from modbus.Simulator import DummySimulator
from modbus.json_types import ReadRequest, WriteRequest


class Handler:

    def __init__(self):
        self.sim = DummySimulator(("localhost", 502))

    async def handleRequest(self, websocket):
        async for message in websocket:
            msg = json.loads(message)
            if "readRequest" in message:
                values = self.sim.makeRequest(ReadRequest.fromJSON(msg))
                await websocket.send(json.dumps(values))
            elif "writeRequest" in message:
                self.sim.makeRequest(WriteRequest.fromJSON(msg))


async def main():
    handler = Handler()

    def wait():
        print("Press any key to exit..")
        input()

    async with websockets.serve(handler.handleRequest, "localhost", 8765):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, wait)

if __name__ == "__main__":
    asyncio.run(main())
