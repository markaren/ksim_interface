from Simulator import Simulator
from modbus.json_types import ReadRequest, WriteRequest


def main():
    
    try:
        sim = Simulator(("localhost", 502))

        result = sim.makeRequest(ReadRequest(address=101, count=6))
        print(f"Got: {result}")
        sim.makeRequest(WriteRequest(address=1, values=[0, 0, 0, 0]))

    except Exception as e:
        print(e)
    

if __name__ == "__main__":
    main()
