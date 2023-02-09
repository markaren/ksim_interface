
import json
import socket
import asyncio
import websockets

from threading import Thread
from modbus.Simulator import Simulator, DummySimulator
from modbus.json_types import ReadRequest, WriteRequest


class Handler:

    def __init__(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sim = DummySimulator(("", 0))
        # self.sim = Simulator(("0.0.0.0", 502))
        self.subs = []

        self.loop = asyncio.get_event_loop()

        def udp():

            async def publish(websocket, data):
                await websocket.send(data)

            try:
                self.sock.bind(("0.0.0.0", 15101))

                while True:
                    data, addr = self.sock.recvfrom(256)
                    dataStr = data.decode("utf-8")
                    tasks = []
                    for sub in self.subs:
                        tasks.append(asyncio.create_task(publish(sub, dataStr)))
                    self.loop.run_until_complete(asyncio.gather(*tasks))
            except:
                self.sock = None

        udpThread = Thread(target=udp)
        udpThread.start()

    def stop(self):
        if self.sock is not None:
            self.sock.close()


    async def handleRequest(self, websocket):
        async for message in websocket:
            msg = json.loads(message)
            requestType = msg["request"]
            if "read" == requestType:
                values = self.sim.makeRequest(ReadRequest.fromJSON(msg))
                try:
                    await websocket.send(json.dumps(values))
                except:
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
        handler.stop()

    async with websockets.serve(handler.handleRequest, "0.0.0.0", 8765):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, wait)

if __name__ == "__main__":
    asyncio.run(main())
