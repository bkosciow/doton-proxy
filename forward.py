import socketserver
import http.server
import socket
from urllib import parse
from http import HTTPStatus

PORT = 9097
bport = 5053
ip_address = '255.255.255.255'

_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


class MyProxy(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        body = parse.parse_qs(body.decode())
        ip = ip_address
        port = bport
        if 'ip' in body and body['ip'][0]:
            ip = body['ip'][0]

        if 'port' in body and body['port'][0]:
            port = body['port'][0]

        _socket.sendto(bytes(body['message'][0].encode('utf-8')), (ip, int(port)))
        self.send_response(HTTPStatus.OK.value)
        self.end_headers()


httpd = socketserver.TCPServer(('', PORT), MyProxy)
print("Serving at", str(PORT))
httpd.serve_forever()

