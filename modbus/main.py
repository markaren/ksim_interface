from pymodbus.client import ModbusTcpClient


def main():
    
    try:
        # Create a Modbus client object
        client = ModbusTcpClient('localhost', port=502)

        # Connect to the Modbus server
        client.connect()
        
        # read registers 101-106
        result = client.read_holding_registers(101, 6, unit=0x01)
        print(result.registers)

        # write registers 1-4
        client.write_registers(1, [0, 0, 0, 0], unit=0x01)

        # Close the connection
        client.close()
    except Exception as e:
        print(e)
    

if __name__=="__main__":
    main()