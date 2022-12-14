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
            data, addr = sock.recvfrom(1024)  # 1024 is the maximum size of a UDP packet

            # Parse the NMEA message using pynmea2
            try:
                msg = pynmea2.parse(data.decode("utf-8"))
            except pynmea2.ParseError:
                # The data is not a valid NMEA message, skip it
                continue

            # At this point, you can access the individual fields of the NMEA message
            # using the properties of the `msg` object. For example:
            print(f"Timestamp: {msg.timestamp}")
            print(f"Latitude: {msg.lat}")
            print(f"Longitude: {msg.lon}")
    except Exception as e:
        print(e)

if __name__=="__main__":
    main
