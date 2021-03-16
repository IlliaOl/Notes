
class HttpRequestParserProtocol:
    def __init__(self, send_response):
        self.send_response = send_response

    def on_url(self, url):
        self.headers = []

    def on_header(self, name, value):
        self.headers.append((name, value))

    def on_body(self, body):
        self.body = body

    def on_message_complete(self):
        self.send_response(self.body)


class SplitBuffer:
    def __init__(self):
        self.data = b""

    def feed_data(self, data):
        self.data += data

    def pop(self, separator):
        first, *rest = self.data.split(separator, maxsplit=1)
        if not rest:
            return None
        else:
            self.data = separator.join(rest)
            return first

    def flush(self):
        temp = self.data
        self.data = b""
        return temp


class HttpRequestParserRequest:
    def __init__(self, protocol):
        self.protocol = protocol
        self.buffer = SplitBuffer()
        self.done_parsing_start = False
        self.done_parsing_headers = False
        self.expected_body_length = 0

    def feed_data(self, data):
        self.buffer.feed_data(data)
        self.parse()

    def parse(self):
        if not self.done_parsing_start:
            self.parse_startline()
        elif not self.done_parsing_headers:
            self.parse_headerline()
        elif self.expected_body_length:
            data = self.buffer.flush()
            self.expected_body_length -= len(data)
            self.protocol.on_body(data)
            self.parse()
        else:
            self.protocol.on_message_complete()

    def parse_startline(self):
        line = self.buffer.pop(separator=b"\r\n")
        if line is not None:
            http_method, url, http_version = line.strip().split()
            self.done_parsing_start = True
            self.protocol.on_url(url)
            self.parse()

    def parse_headerline(self):
        line = self.buffer.pop(separator=b"\r\n")
        if line is not None:
            if line:
                name, value = line.strip().split(b": ", maxsplit=1)
                if name.lower() == b"content-length":
                    self.expected_body_length = int(value.decode("utf-8"))
                self.protocol.on_header(name, value)
            else:
                self.done_parsing_headers = True
            self.parse()


class HttpRequestParserResponse:
    def __init__(self, protocol):
        self.protocol = protocol
        self.buffer = SplitBuffer()
        self.done_parsing_start = False
        self.done_parsing_headers = False
        self.expected_body_length = 0

    def feed_data(self, data):
        self.buffer.feed_data(data)
        self.parse()

    def parse(self):
        if not self.done_parsing_start:
            self.parse_startline()
        elif not self.done_parsing_headers:
            self.parse_headerline()
        elif self.expected_body_length:
            data = self.buffer.flush()
            self.expected_body_length -= len(data)
            self.protocol.on_body(data)
            self.parse()
        else:
            self.protocol.on_message_complete()

    def parse_startline(self):
        line = self.buffer.pop(separator=b"\r\n")
        if line is not None:
            http_version, code = line.strip().split()
            self.done_parsing_start = True
            self.protocol.on_url(code)
            self.parse()

    def parse_headerline(self):
        line = self.buffer.pop(separator=b"\r\n")
        if line is not None:
            if line:
                name, value = line.strip().split(b": ", maxsplit=1)
                if name.lower() == b"content-length":
                    self.expected_body_length = int(value.decode("utf-8"))
                self.protocol.on_header(name, value)
            else:
                self.done_parsing_headers = True
            self.parse()


class Response:
    def create_status_line(self, status_code):
        code = str(status_code).encode()
        return b"HTTP/1.1 " + code + b"\r\n"

    def format_headers(self, l):
        headers = [
            b"Server: Apache/2.2.14 (win32)\r\n",
            b"Connection: Closed\r\n"]
        if l:
            headers.append(b"Content-Length: " + l + b"\r\n")
        return b"".join(headers)

    def make_response(self, status_code, body):
        length = 0
        if body:
            length = (str(len(body)).encode("utf-8"))
        content = [
            self.create_status_line(status_code),
            self.format_headers(length),
            b"\r\n" if body else b"",
            body,
        ]
        return b"".join(content)


class Request:
    def create_status_line(self, verb):
        verb = verb.encode()
        return verb + b" / HTTP/1.1" + b"\r\n"

    def format_headers(self, l):
        headers = [
            b"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n",
            b"Host: localhost\r\n",
            b"Accept-Language: en-us\r\n",
            b"Connection: keep-alive\r\n"]
        if l:
            headers.append(b"Content-Length: " + l + b"\r\n")
        return b"".join(headers)

    def make_request(self, verb, body):
        length = 0
        if body:
            length = (str(len(body)).encode("utf-8"))
        content = [
            self.create_status_line(verb),
            self.format_headers(length),
            b"\r\n" if body else b"",
            body,
        ]
        return b"".join(content)
