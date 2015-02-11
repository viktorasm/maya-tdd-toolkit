import sys
from dccautomation import configs as dcconf
from dccautomation import inproc

def runTestsInMaya(testsRootPackageName,testName=None):
    '''
    execute this from IDE
    '''
    print "executing tests in maya .."
    
    client = inproc.start_inproc_client(dcconf.Maya2015OSX(), 9025)
    
    command = 'import mayatdd.client as mayatddclient;reload(mayatddclient);mayatddclient.launch('+repr(testsRootPackageName)+','+repr(testName)+');'
    client.exec_(command)
    print "----------------------------------------------------------------------"
    print client.eval_('mayatddclient.lastTestExecutionOutput')
    
