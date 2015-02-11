import sys
from dccautomation import configs as dcconf
from dccautomation import inproc

def runTestsInMaya(testsRootModuleName,testName=None):
    '''
    execute this from IDE
    '''
    print "executing tests in maya .."
    
    client = inproc.start_inproc_client(dcconf.Maya2015OSX(), 9025)
    
    command = 'import maya_tdd.client as maya_tdd_client;maya_tdd_client.launch('+repr(testsRootModuleName)+','+repr(testName)+');'
    client.exec_(command)
    print "----------------------------------------------------------------------"
    print client.eval_('maya_tdd_client.lastTestExecutionOutput')
    
    
if __name__ == '__main__':
    runTestsInMaya(*sys.argv[1:])
    
