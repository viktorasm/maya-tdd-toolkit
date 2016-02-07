'''
simple RPC over HTTP
'''

import SimpleHTTPServer
import SocketServer
import threading
import json
import urllib2

class Client:
    def __init__(self,host,port):
        self.timeout = 300
        self.endpoint = "http://{0}:{1}".format(host,port)
        
    def send(self,jsonDictionary):
        '''
        sends JSON over the HTTP POST and returns parsed JSON as result
        
        no particular error checking is done as we trust our server in a way.
        '''
        data = json.dumps(jsonDictionary)
        response = urllib2.urlopen(self.endpoint, data=data, timeout=self.timeout)
        return json.loads(response.read())
        

class Server:
    def __init__(self,port):
        self.port = port
    
    def run(self, requestHandlerMethod):
        class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
            instance = None
        
            def do_GET(self):
                self.wfile.write("maya tdd server\n")
        
            def do_POST(self):
                request = self.rfile.read(int(self.headers['Content-Length']))
                request = json.loads(request)
                result = requestHandlerMethod(request)
                self.wfile.write(json.dumps(result))
            
        self.instance = SocketServer.TCPServer(("", self.port), RequestHandler) 
        threading.Thread(target=self.instance.serve_forever).start()
    
    def stop(self):
        self.instance.shutdown()
        