import unittest

from mayatdd import server


class ServerTest(unittest.TestCase):
    def setUp(self):
        self.server = None
        self.port = 6778
        self.server = server.Server(self.port)

    def testConnect(self):
        '''
        validate that server-client connection is happening and that handler is installed correctly
        '''

        def fakeHandler(request):
            if "validRequest" in request:
                return {'response': request['validRequest']}
            else:
                return 'not the right thing received'

        self.server.run(fakeHandler)

        for i in range(100):
            client = server.Client("127.0.0.1", self.port)
            result = client.send({'validRequest': i})
            self.assertEqual(result, {'response': i})

    def tearDown(self):
        if self.server is not None:
            self.server.stop()
