'''
simple RPC over HTTP
'''

import threading
import json
import socket

try:
    from BaseHTTPServer import BaseHTTPRequestHandler
    from SocketServer import TCPServer
except:
    from http.server import BaseHTTPRequestHandler
    from socketserver import TCPServer


class Client:
    def __init__(self, host, port):
        self.timeout = 300
        self.endpoint = "http://{0}:{1}".format(host, port)

    def send(self, jsonDictionary):
        '''
        sends JSON over the HTTP POST and returns parsed JSON as result
        
        no particular error checking is done as we trust our server in a way.
        '''
        data = json.dumps(jsonDictionary).encode("utf-8")

        try:
            from urllib2 import urlopen
        except:
            from urllib.request import urlopen

        response = urlopen(self.endpoint, data=data, timeout=self.timeout)
        return json.loads(response.read())


class Server:

    def __init__(self, port):
        self.port = port
        self.instance = None
        self.instance_thread = None

    def run(self, requestHandlerMethod):
        class RequestHandler(BaseHTTPRequestHandler):

            def do_GET(self):
                self.wfile.write("maya tdd server\n")

            def do_POST(self):
                request = self.rfile.read(int(self.headers['Content-Length']))
                request = json.loads(request)
                result = requestHandlerMethod(request)

                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(result).encode("utf-8"))

        self.instance = TCPServer(("", self.port), RequestHandler, bind_and_activate=False)
        self.instance.allow_reuse_address = True
        self.instance.server_bind()
        self.instance.server_activate()
        self.instance_thread = threading.Thread(target=self.instance.serve_forever)
        self.instance_thread.start()

    def stop(self):
        if self.instance is not None:
            self.instance.shutdown()
            self.instance_thread.join()
            self.instance.server_close()
