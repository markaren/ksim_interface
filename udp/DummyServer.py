import socket
from threading import Thread

if __name__ == "__main__":

    stop = False

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def serve():
        while not stop:
            for i in range(0, 10):
                sock.sendto(f"test{i}".encode("utf-8"), ("localhost", 15101))

    t = Thread(target=serve)
    t.start()

    print("Press any key to exit..")
    input()
    stop = True
