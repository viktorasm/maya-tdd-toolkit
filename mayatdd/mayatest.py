from functools import wraps
import inspect
import sys
import importlib
import random
import pickle
import base64

try:
    from maya import cmds
    # just assume that if cmds is available, we're inside maya
    insideMaya = cmds.about(version=True) is not None
except:
    insideMaya = False

def outputRedirect(func):
    def wrapped(*args,**kwargs):
        backupStdOut = sys.stdout
        backupStdErr = sys.stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stdout__
        try:
            return func(*args,**kwargs)
        finally:
            sys.__stdout__.flush()
            sys.stdout = backupStdOut
            sys.stderr = backupStdErr
    return wrapped

def dropCachedImports(*packagesToUnload):
    '''
    prepares maya to re-import 
    '''
    
    def shouldUnload(module):
        for packageToUnload in packagesToUnload:
            if module.startswith(packageToUnload):
                return True
        return False
        
    
    for i in sys.modules.keys()[:]:
        if shouldUnload(i):
            #print "unloading module ", i
            del sys.modules[i] 
            


currentTestSuite = random.randint(0,0xFFFF)

@outputRedirect
def launch(testSuiteId,sysPath,setupModuleName,moduleName,className,testMethodName):
    '''
    this method gets called from within maya with current test class and method name
    '''

    splitter = "-- TEST: "+className+"."+testMethodName
    splitter += '-'*(80-len(splitter))+"\n"
    sys.__stdout__.write(splitter)        

    
    for sp in sysPath:
        if sp not in sys.path:
            sys.path.append(sp)
            
    # check if current test suite changed, and run setup fo this suite if needed
    suiteIdVar='mayatdd_currentTestSuite'
    if not cmds.optionVar(exists=suiteIdVar) or cmds.optionVar(q=suiteIdVar)!=testSuiteId:
        cmds.optionVar(iv=(suiteIdVar,testSuiteId))

        setupModule = importlib.import_module(setupModuleName)
        reload(setupModule)

        if hasattr(setupModule, 'cleanUp'):
            print "running tests cleanup hook"
            setupModule.cleanUp()

        # reload modules
        print "running reloads"
        dropCachedImports(*setupModule.reloadModules)
        
        # run one-time setup.py tests
        if hasattr(setupModule, 'setup'):
            print "running tests setup hook"
            setupModule.setup()
    
    targetModule = importlib.import_module(moduleName)
    targetClass = getattr(targetModule, className)
    
    targetInstance = targetClass(testMethodName)

    try:
        targetInstance.setUp()
        getattr(targetInstance, testMethodName)()
        targetInstance.tearDown()
    except:
        import traceback;traceback.print_exc()
        
def serverHandler(request):
    def mainThreadHandler(request):
        try:
            launch(**request)
            return {'result':'success'}
        except Exception,e:
            import traceback;traceback.print_exc()
            #return {'result':'exception','exception':pickle.dumps(e, pickle.HIGHEST_PROTOCOL)}
            return {'result':'exception','exception':base64.b64encode(pickle.dumps(e, pickle.HIGHEST_PROTOCOL)),'stackTrace':traceback.format_exc()}
        
    from maya.utils import executeInMainThreadWithResult
    return executeInMainThreadWithResult(mainThreadHandler,request) 
    
def mayaTest(setupModule):
    setupModule = sys.modules[setupModule]
    
    def decorator(cls):
        if not insideMaya:
            voidMethod = lambda *args,**kwargs:None
            setattr(cls,'setUp',voidMethod)
            setattr(cls, "tearDown", voidMethod)
            
        
        for methodName,method in list(inspect.getmembers(cls, inspect.ismethod))[:]:
            if not methodName.startswith("test"):
                continue
    
            if insideMaya:
                decorated = method
                
            else:   
                def createDecoratedMethod(methodName,method):     
                    def decorated(*args,**kwargs):
                        import server
                        client = server.Client("localhost", 9025)
                        
                        sysPath = [] if not hasattr(setupModule, 'sysPath') else setupModule.sysPath

                        print "running {}.{}...".format(cls.__name__,methodName)
                        global currentTestSuite
                        
                        response = client.send({
                            'testSuiteId': currentTestSuite,
                            'sysPath': sysPath,
                            'setupModuleName': setupModule.__name__,
                            'moduleName': cls.__module__, 
                            'className': cls.__name__,
                            'testMethodName': methodName
                        })
                        if response['result']=='exception':
                            print response['stackTrace']
                            raise pickle.loads(base64.b64decode(response['exception']))
                            
                        print "done executing",cls.__name__+'.'+methodName
                    return wraps(method)(decorated)
                decorated = createDecoratedMethod(methodName, method)
            setattr(cls,methodName,decorated)
        
        return cls
    return decorator