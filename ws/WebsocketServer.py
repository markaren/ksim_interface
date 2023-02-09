
import json
import asyncio
import websockets

from modbus.Simulator import DummySimulator
from modbus.json_types import ReadRequest, WriteRequest


class Handler:

    def __init__(self):
        self.sim = DummySimulator(("localhost", 502))
        self.subs = []

    async def handleRequest(self, websocket):
        async for message in websocket:
            msg = json.loads(message)
            requestType = msg["request"]
            if "read" == requestType:
                values = self.sim.makeRequest(ReadRequest.fromJSON(msg))
                try:
                    await websocket.send(json.dumps(values))
                except Exception:
                    if websocket in self.subs:
                        self.subs.remove(websocket)

            elif "write" == requestType:
                self.sim.makeRequest(WriteRequest.fromJSON(msg))
            elif "subscribe" == requestType:
                self.subs.append(websocket)


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
