'''
simple RPC over HTTP
'''

import SimpleHTTPServer
import SocketServer
import threading
import json
import urllib2
import struct

class JsonStream:
    def __init__(self,sock):
        '''
        :param sock: socket.socket 
        '''
        print repr(sock)
        self.sock = sock
        self.rfile = self.sock.makefile('rb', 1024)
        self.wfile = self.sock.makefile('wb', 1024)
        
    def sendJson(self,doc):
        #self.wfile.writelines([json.dumps(doc)])
        self.wfile.write("asdf\n")
        
        
    def readJson(self):
        #return json.dumps(self.rfile.readline())
        return self.rfile.readline()
        

class Client:
    def __init__(self,host,port):
        import socket
        self.sock = socket.create_connection((host,port))
        self.jsonStream = JsonStream(self.sock)
        
    def send(self,jsonDictionary):
        '''
        sends JSON over the HTTP POST and returns parsed JSON as result
        
        no particular error checking is done as we trust our server in a way.
        '''
        print "client: sending json"
        self.jsonStream.sendJson(jsonDictionary)
        print "client: json sent"
        
        print "client: reading json"
        return self.jsonStream.readJson()
        

class Server:
    def __init__(self,port):
        self.port = port
    
    def run(self, requestHandlerMethod):
        
        class JsonStreamHandler(SocketServer.StreamRequestHandler):
            def handle(self):
                print "server handling"
                print self.rfile.readline()
                print "input read"
                self.wfile.writelines(["you fail"])
                self.wfile.flush()
                return
                print "handling stuff"
                h = JsonStream(self.request)
                data = h.readJson()
                print "data received",data
                result = requestHandlerMethod(data)
                h.sendJson(result)
                
        self.instance = SocketServer.TCPServer(("", self.port), JsonStreamHandler) 
        threading.Thread(target=self.instance.serve_forever).start()
    
    def stop(self):
        self.instance.shutdown()
        