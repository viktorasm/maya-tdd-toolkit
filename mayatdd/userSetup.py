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
    
import dccautomation
from dccautomation import configs as dcconf

info("Starting dccautomation server...")

dccautomation.start_inproc_server(dcconf.Maya2015OSX(), 9025)

info("Maya is ready for some tests!")
