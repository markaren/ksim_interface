
import json
import socket
from threading import Thread
from pymodbus.client import ModbusTcpClient
from json_types import ReadRequest, WriteRequest


class ModbusWrapper:

    def __init__(self, port: int):
        self.client = ModbusTcpClient('localhost', port=port)
        self.client.connect()

    def makeRequest(self, request):
        if isinstance(request, ReadRequest):
            return self.client.read_holding_registers(request.address, request.count, unit=0x01)
        elif isinstance(request, WriteRequest):
            self.client.write_registers(request.address, request.values, unit=0x01)
        else:
            print(f"Error: illegal request: {request}")

    def close(self):
        self.client.close()


# used for testing
class DummyModbusWrapper(ModbusWrapper):

    def __init__(self, port):
        self.values = [1, 2, 3, 4, 5]

    def makeRequest(self, request):
        if isinstance(request, ReadRequest):
            return self.values[request.address : request.address+request.count]
        elif isinstance(request, WriteRequest):
            self.values = request.values

    def close(self):
        pass


class ServerSocket:

    def __init__(self, port: int):
        server_address = ('localhost', port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(server_address)

        print("Serving connections on port {}".format(server_address[1]))
        self.sock.listen()

        self.sim = ModbusWrapper(502)

        def accept():
            try:
                while True:
                    conn, addr = self.sock.accept()
                    print(f"Connected by {addr}")
                    t = Thread(target=self._connectionHandler, args=(conn,))
                    t.start()
            except Exception as e:
                pass

        self.acceptorThread = Thread(target=accept)
        self.acceptorThread.start()

    def _connectionHandler(self, conn):

        def write(values):
            data = json.dumps(values).encode("utf-8")
            conn.send(len(data).to_bytes(4, byteorder="little"))
            conn.send(data)

        def read():
            msgSize = int.from_bytes(conn.recv(4), byteorder="little")
            recv = conn.recv(msgSize).decode("utf-8")
            msg = json.loads(recv)
            return msg

        try:
            while True:
                msg = read()
                if "readRequest" in msg:
                    req = ReadRequest.fromJSON(msg)
                    values = self.sim.makeRequest(req)
                    write(values)
                elif "writeRequest" in msg:
                    req = WriteRequest.fromJSON(msg)
                    self.sim.makeRequest(req)
        except Exception as e:
            print("Client disconnected")
            conn.close()

    def close(self):
        self.sock.close()


def main():

    try:
        ss = ServerSocket(9090)
        print("Press any key to exit..")
        input()
        ss.close()
    except Exception as e:
        pass


if __name__ == "__main__":
    main()
