'''
this module will be copied into launched maya's /scripts folder
'''

import sys
import os

def info(message):
    print message
    sys.stdout.flush()

info("Configuring Maya for test execution..")


testPythonPath = os.environ.get('maya_test_pythonpath') 
if testPythonPath is not None:
    for i in testPythonPath.split(";"):
        info("adding python path: "+i)
        sys.path.append(i)

from mayatdd import mayatest, server

info("Starting TDD server...")
server.Server(9025).run(mayatest.serverHandler)
info("Maya is ready for some tests!")
