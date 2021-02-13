from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import json


host = "localhost"
port = 8080
queue = 16


def connection(csocket):
    client_msg = json.loads(csocket.recv(1024).decode())
    response = json.dumps({"result": str(2 * int(client_msg["N"]) / 13), "thread": client_msg["request"]}).encode()
    csocket.send(response)
    csocket.close()


def main():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((host, port))
    s.listen(queue)

    while True:
        clientsocket, address = s.accept()
        t = Thread(target=connection, args=(clientsocket,))
        t.start()


if __name__ == '__main__':
    main()
