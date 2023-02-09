from pymodbus.client import ModbusTcpClient
from modbus.json_types import ReadRequest, WriteRequest


class Simulator:

    def __init__(self, address: (str, int)):
        self.client = ModbusTcpClient(address[0], port=address[1])
        self.client.connect()

    def makeRequest(self, request):
        if isinstance(request, ReadRequest):
            values = self.client.read_holding_registers(request.address, request.count, unit=0x01).registers
            map = {}
            index = 0
            for register in range(request.address, request.address+request.count):
                map[register] = values[index]
                index = index + 1
            return map
        elif isinstance(request, WriteRequest):
            self.client.write_registers(request.address, request.values, unit=0x01)
        else:
            print(f"Error: illegal request: {request}")

    def close(self):
        self.client.close()


# used for testing
class DummySimulator(Simulator):

    def __init__(self, address):
        self.values = [0] * 1000

    def makeRequest(self, request):
        if isinstance(request, ReadRequest):
            map = {}
            for register in range(request.address, request.address+request.count):
                map[register] = self.values[register]
            return map
        elif isinstance(request, WriteRequest):
            self.values[request.address: request.address + len(request.values)] = request.values

    def close(self):
        pass
