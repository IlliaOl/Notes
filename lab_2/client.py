from socket import socket, AF_INET, SOCK_STREAM, SO_RCVBUF, SOL_SOCKET
from threading import Thread
from .http import *
import json
import random

IP = "localhost"
PORT = 8080
QUEUE = 16


def connect(i):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((IP, PORT))
    request_msg = json.dumps({"N": random.randint(1, 100), "request": i}).encode()
    request = Request()
    s.send(request.make_request("GET", request_msg))

    def print_result(m):

        message = json.loads(m.decode())
        print(message["result"], "|", message["request"])

    protocol = HttpRequestParserProtocol(print_result)
    parser = HttpRequestParserResponse(protocol)
    data = read(s)
    parser.feed_data(data)
    s.close()


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
