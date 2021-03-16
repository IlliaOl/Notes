from http_classes import *
import socket
import select
import json


IP = "localhost"
PORT = 8080
QUEUE = 16
BUFFER_SIZE = 1024


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setblocking(False)

    server_socket.bind((IP, PORT))
    server_socket.listen(QUEUE)

    inputs = [server_socket]
    outputs = []
    messages = {}

    while True:
        read_sockets, write_sockets, exception_sockets = select.select(inputs, outputs, inputs)
        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                client_socket.setblocking(False)
                inputs.append(client_socket)
            else:
                data = notified_socket.recv(BUFFER_SIZE)
                if data:
                    messages[notified_socket] = data
                    if notified_socket not in outputs:
                        outputs.append(notified_socket)
                else:
                    if notified_socket in outputs:
                        outputs.remove(notified_socket)
                    inputs.remove(notified_socket)
                    del messages[notified_socket]
                    notified_socket.close()
        for notified_socket in write_sockets:
            def send_response(m):
                message = json.loads(m.decode())
                result = json.dumps({"result": str(2 * int(message["N"]) / 13), "request": message["request"]}).encode()
                response = Response()
                notified_socket.send(response.make_response(200, result))

            protocol = HttpRequestParserProtocol(send_response)
            parser = HttpRequestParserRequest(protocol)
            parser.feed_data(messages[notified_socket])
            if notified_socket in inputs:
                inputs.remove(notified_socket)
            outputs.remove(notified_socket)
            notified_socket.close()

        for notified_socket in exception_sockets:
            inputs.remove(notified_socket)
            if notified_socket in outputs:
                outputs.remove(notified_socket)
            del messages[notified_socket]
            notified_socket.close()


if __name__ == '__main__':
    main()
