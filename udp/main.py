import time
import socket
import pynmea2

UDP_IP = "0.0.0.0"  # Listen on all available network interfaces
UDP_PORT = 15101 


def main():
    
    try:
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to the IP and port
        sock.bind((UDP_IP, UDP_PORT))

        while True:
            # Receive data from the socket
            data, addr = sock.recvfrom(256)  # 1024 is the maximum size of a UDP packet

            dataStr = data.decode("utf-8")
            
            if dataStr.startsWith("$"):
                try:
                    # Parse the NMEA message using pynmea2
                    msg = pynmea2.parse(dataStr)
                except pynmea2.ParseError as e:
                    # The data is not a valid NMEA message, skip it
                    print(e)
                    break
            else:
                print(dataStr)

    except Exception as e:
        print(e)

if __name__=="__main__":
    main
