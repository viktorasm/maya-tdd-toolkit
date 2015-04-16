from functools import wraps
import inspect
import sys
import importlib
insideMaya = False

try:
    from maya import cmds
    # just assume that if cmds is available, we're inside maya
    insideMaya = True
except:
    pass

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

def decorateMayaTest(method):
    m = method
    def decorated(*args,**kwargs):
        splitter = "-- TEST: "+m.im_class.__name__+"."+m.__name__
        splitter += '-'*(80-len(splitter))+"\n"
        sys.__stdout__.write(splitter)        
        return m(*args,**kwargs);
    return decorated

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

@outputRedirect
def launch(sysPath,setupModuleName,moduleName,className,testMethodName):
    '''
    this gets called from within maya
    '''
    for sp in sysPath:
        if sp not in sys.path:
            sys.path.append(sp)
            
    setupModule = importlib.import_module(setupModuleName)
    reload(setupModule)
    dropCachedImports(*setupModule.reloadModules)
    
    targetModule = importlib.import_module(moduleName)
    targetClass = getattr(targetModule, className)
    
    targetInstance = targetClass(testMethodName)
    
    try:
        targetInstance.setUp()
        getattr(targetInstance, testMethodName)()
    except:
        import traceback;traceback.print_exc()
        raise
    
def mayaTest(setupModule):
    setupModule = sys.modules[setupModule]
    
    def decorator(cls):
        
        for methodName,method in list(inspect.getmembers(cls, inspect.ismethod))[:]:
            if not methodName.startswith("test"):
                continue
    
            if insideMaya:
                decorated = decorateMayaTest(method)
                
            else:        
                @wraps(method)
                def decorated(*args,**kwargs):
                    from dccautomation import inproc
                    from dccautomation import configs as dcconf                    
                    client = inproc.start_inproc_client(dcconf.Maya2015OSX(), 9025)
                    
                    sysPath = [] if not hasattr(setupModule, 'sysPath') else setupModule.sysPath
                    
                    command = 'import mayatdd.mayatest as mayatest;reload(mayatest);'+ \
                        'mayatest.launch({!r},{!r},{!r},{!r},{!r})'.format(sysPath,setupModule.__name__,cls.__module__,cls.__name__,methodName)
                        
                    client.exec_(command)
                    print "done executing",cls.__name__+'.'+methodName
                
            setattr(cls,methodName,decorated)
        
        return cls
    return decorator