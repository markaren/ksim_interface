from pymodbus.client import ModbusTcpClient
import socket
import json


class ModbusWrapper:

    def __init__(self, port: int):
        self.client = ModbusTcpClient('localhost', port=port)
        self.client.connect()

    def write(self, address: int, values):
        self.client.write_registers(address, values, unit=0x01)

    def read(self, address: int, count: int = 1):
        return self.client.read_holding_registers(address, count, unit=0x01)

    def close(self):
        self.client.close()


class Socket:

    def __init__(self, port: int):
        server_address = ('localhost', port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(server_address)

        print("Serving connections on port {}".format(server_address[1]))
        self.sock.listen()

        self.conn, addr = self.sock.accept()
        print(f"Connected by {addr}")

    def write(self, values):
        data = json.dumps(values)
        self.conn.send(len(data).to_bytes(4, byteorder="little"))
        self.conn.send(data)

    def read(self):
        msgSize = int.from_bytes(self.conn.recv(4), byteorder="little")
        msg = json.loads(self.conn.recv(msgSize).decode("utf-8"))
        return msg

    def close(self):
        self.conn.close()
        self.sock.close()


def main():

    try:
        conn = Socket(9090)
        sim = ModbusWrapper(502)

        while True:
            msg = conn.read()
            if "readRequest" in msg:
                address = msg.readRequest.address
                count = msg.readRequest.count
                values = sim.read(address, count)
                sim.write(address, values)
            elif "writeRequest" in msg:
                address = msg.data.address
                values = msg.data.values
                sim.write(address, values)
    except Exception as e:
        print(e)
    

if __name__ == "__main__":
    main()
