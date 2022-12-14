from pymodbus.client.sync import ModbusTcpClient


def main():
    
    try:
        # Create a Modbus client object
        client = ModbusTcpClient('localhost', port=502)

        # Connect to the Modbus server
        client.connect()
        
        # read registers 1-4
        result = client.read_holding_registers(1, 4, unit=0x01)
        print(result.registers)

        # write registers 101-106
        #client.write_registers(101, [0, 0, 0, 0, 0, 0], unit=0x01)

        # Close the connection
        client.close()
    except Exception as e:
        print(e)
    

if __name__=="__main__":
    main()