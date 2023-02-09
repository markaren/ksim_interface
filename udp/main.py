import time
import socket


def main():
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", 15101))

        while True:
            # Receive data from the socket
            data, addr = sock.recvfrom(256)
            dataStr = data.decode("utf-8")
            print(dataStr)
            
            time.sleep(0.1)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
