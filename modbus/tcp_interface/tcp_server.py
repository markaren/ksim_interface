
import json
import socket
from threading import Thread
from modbus.Simulator import Simulator
from modbus.json_types import ReadRequest, WriteRequest


class ServerSocket:

    def __init__(self, port: int):
        server_address = ('localhost', port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(server_address)

        print("Serving connections on port {}".format(server_address[1]))
        self.sock.listen()

        self.sim = Simulator(("localhost", 502))

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
                    response = self.sim.makeRequest(req)
                    write(response)
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
