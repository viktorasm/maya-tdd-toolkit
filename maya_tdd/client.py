import sys
import StringIO
import unittest
import os
import inspect
import importlib

def runSuite(suite):
    '''
    runs provided test suite inside current python interpreter,
    capturing all test output into module global 'lastTestExecutionOutput'
    '''
    global lastTestExecutionOutput
    lastTestExecutionOutput = ''
    try:
        output = StringIO.StringIO()
        backupStdOut = sys.stdout
        backupStdErr = sys.stderr
        try:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stdout__
            unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
            lastTestExecutionOutput = output.getvalue()
        finally:
            sys.__stdout__.flush()
            sys.stdout = backupStdOut
            sys.stderr = backupStdErr
        
    except:
        lastTestExecutionOutput = "Tests failed to finish"
        raise
        

def isTestsClass(c):
    '''
    it's a test class if it inherits test case and has at least one test*() method
    '''
    if not issubclass(c, unittest.TestCase):
        return False
    
    for method,_ in inspect.getmembers(c, inspect.ismethod):
        if method.startswith("test"):
            return True
    
    return False; 

def decorateTestMethods(c):
   
    
    allTestMethods = []
    
    for methodName,method in list(inspect.getmembers(c, inspect.ismethod))[:]:
        if not methodName.startswith("test"):
            continue
        
        allTestMethods.append(methodName)
        
        def decorate(method):
            m = method
            def decorated(*args,**kwargs):
                splitter = "-- TEST: "+m.im_class.__name__+"."+m.__name__
                splitter += '-'*(80-len(splitter))+"\n"
                sys.__stdout__.write(splitter)        
                return m(*args,**kwargs);
            return decorated

        setattr(c, methodName, decorate(method))
        
    return allTestMethods

def dropCachedImports(*modulesToUnload):
    
    def shouldUnload(module):
        for moduleToUnload in modulesToUnload:
            if module.startswith(moduleToUnload):
                return True
        return False
        
    
    for i in sys.modules.keys()[:]:
        if shouldUnload(i):
            print "unloading module ", i
            del sys.modules[i]   

def launch(testsRootModuleName,testName):
    '''
    testsAll: module importing all suite tests;
    testName: None for all tests; Class.testName for single test launch; <Class> for all tests in a class
    '''
    rootModule = importlib.import_module(testsRootModuleName)
    setup = importlib.import_module(testsRootModuleName+'.setup')
    dropCachedImports(*setup.reloadModules)
    
    packageRoot = os.path.dirname(rootModule.__file__)
    print "launching tests from",packageRoot
    

    singleClass = None # all
    singleMethod = None # all
    if testName is not None:
        testName = testName.split(".");
        singleClass = testName[0]
        if len(testName)>1:
            singleMethod = testName[1]
            
    testSuite = unittest.TestSuite()
    
    def discoverTestsInClass(c):
        testMethods = decorateTestMethods(c)
        for testMethod in testMethods:
            if singleMethod is not None and testMethod!=singleMethod:
                continue

            testSuite.addTest(c(testMethod))  
            
    def discoverTestsInModule(module):  
        for _,c in inspect.getmembers(module, inspect.isclass):
            if singleClass is not None and c.__name__!=singleClass:
                continue
            
            if isTestsClass(c):
                discoverTestsInClass(c)
                                
    for root, dirs, files in os.walk(packageRoot):
        if root==packageRoot:
            fromList = testsRootModuleName
        else:
            fromList = testsRootModuleName+'.'+root[len(packageRoot)+1:].replace(os.sep,".")
            
        print root
        
        for f in files:
            if f.endswith(".py"):
                try:
                    module = importlib.import_module(fromList+'.'+f[:-3])
                except:
                    print "import fail"
                    # import fail - whatever.
                    continue;
                
                discoverTestsInModule(module);

    
    runSuite(testSuite)