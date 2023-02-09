
import asyncio
import websockets

from modbus.json_types import ReadRequest, WriteRequest


async def hello():
    # address = "ws://10.24.92.77:8765"
    address = "ws://localhost:8765"
    async with websockets.connect(address) as websocket:
        await websocket.send(WriteRequest(address=1, values=[10, 14]).toJSON())
        await websocket.send(ReadRequest(address=101, count=6).toJSON())
        values = await websocket.recv()
        print(values)


if __name__ == "__main__":
    asyncio.run(hello())
