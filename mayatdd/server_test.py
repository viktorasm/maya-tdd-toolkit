import unittest
import server



class ServerTest(unittest.TestCase):
    def setUp(self):
        self.port = 6777 
        self.server = server.Server(self.port)
        
    def testConnect(self):
        '''
        validate that server-client connection is happening and that handler is installed correctly
        '''
        def fakeHandler(request):
            if request=={'a':'b'}:
                return {'c':'d'}
            else:
                return 'not the right thing received'
            
        self.server.run(fakeHandler)

        client = server.Client("127.0.0.1",self.port)
        result = client.send({'a':'b'})
        self.assertEquals(result, {'c':'d'})
        
    def tearDown(self):
        self.server.stop()
        
