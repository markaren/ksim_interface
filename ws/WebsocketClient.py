
import asyncio
import websockets

from modbus.json_types import ReadRequest, WriteRequest


async def hello():
    async with websockets.connect("ws://localhost:8765") as websocket:
        await websocket.send(WriteRequest(address=1, values=[10, 14]).toJSON())
        await websocket.send(ReadRequest(address=1, count=2).toJSON())
        values = await websocket.recv()
        print(values)


if __name__ == "__main__":
    asyncio.run(hello())