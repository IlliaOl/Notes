from socket import socket, AF_INET, SOCK_STREAM, SO_RCVBUF, SOL_SOCKET
import json
import random


host = "localhost"
port = 8080
requests = 16


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
    for i in range(1, requests+1):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((host, port))
        msg = {"N": random.randint(1, 100), "request": i}
        request_msg = json.dumps(msg).encode()
        s.send(request_msg)
        server_msg = json.loads(read(s).decode())
        s.close()
        print(f"{server_msg['result']} | {server_msg['thread']}")


if __name__ == '__main__':
    main()
