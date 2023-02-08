
import json
import socket
from modbus.json.json_types import ReadRequest, WriteRequest


class ClientSocket:

    def __init__(self, server_address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Connecting to {} port {}".format(server_address[0], server_address[1]))
        self.sock.connect(server_address)

    def write(self, address: int, values):
        self._writeRequest(WriteRequest(address, values))

    def read(self, address: int, count: int):
        self._writeRequest(ReadRequest(address, count))
        msgSize = int.from_bytes(self.sock.recv(4), byteorder="little")
        msg = json.loads(self.sock.recv(msgSize).decode("utf-8"))
        return msg

    def _writeRequest(self, request):
        data = request.toJSON().encode("utf-8")
        self.sock.send(len(data).to_bytes(4, byteorder="little"))
        self.sock.send(data)

    def close(self):
        self.sock.close()


def main():

    sock = ClientSocket(("localhost", 9090))
    values = sock.read(address=101, count=6)
    print(f"Got: {values}")
    sock.write(address=1, values=[0, 0, 0, 0])
    sock.close()


if __name__ == "__main__":
    main()
