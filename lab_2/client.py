from socket import socket, AF_INET, SOCK_STREAM, SO_RCVBUF, SOL_SOCKET
from threading import Thread
import json
import random
import re

IP = "localhost"
PORT = 8080
QUEUE = 16


def send_message(sct, message):
    http = f"HTTP/1.1 200 OK \r\nContent-Type: text/html; " + \
           f"charset=utf-8 \r\n\r\n{message}"

    sct.sendall(http.encode())


def receive_message(message):
    m = re.search(r"\s([{\[].*?[}\]])$", message.decode()).group(1)
    m = json.loads(m)
    return m


def connect(i):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((IP, PORT))
    request_msg = json.dumps({"N": random.randint(1, 100), "request": i})
    send_message(s, request_msg)
    response = read(s)
    server_msg = receive_message(response)
    s.close()
    print(f"{server_msg['result']} | {server_msg['request']}")


def read(s):
    msg = bytearray()
    buffer_size = s.getsockopt(SOL_SOCKET, SO_RCVBUF)
    while True:
        chunk = s.recv(buffer_size)
        if chunk:
            msg += chunk
        if len(chunk) == 0 or chunk[-1:] == b'\n':
            break
    return msg


def main():
    for i in range(1, QUEUE+1):
        t = Thread(target=connect, args=(i,))
        t.start()


if __name__ == '__main__':
    main()
