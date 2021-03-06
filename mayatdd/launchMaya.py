'''
launch maya with settings that will enable launching tests with provided scripts;
feedbacks all stdout output back to IDE
'''
import subprocess
import os
import shutil

import platform

class Launcher:
    def __init__(self):
        self.isWindows = 'windows' in platform.system().lower()
        self.isLinux = 'linux' in platform.system().lower()
            
        self.mayaExecutable=os.path.join(os.environ['MAYA_HOME'],'bin','maya')
        if self.isWindows:
            self.mayaExecutable += ".exe"
        
        self.mayaPath = None
        self.projectDir = os.path.abspath(os.path.dirname(__file__)+"/..")
        self.mayaEnvTemplateDir = self.projectDir+'/testMayaLaunchEnvironment_snapshot'
        self.projectWorkspace = os.path.abspath(os.path.dirname(__file__)+"/../../")
        
        # add dcc automation
        self.pythonPath = []
        # add self to path
        self.pythonPath.append(self.projectDir)
        # add site-packages
        from distutils.sysconfig import get_python_lib; 
        self.pythonPath.append(get_python_lib())
        
        self.parseCommandLine()
            
    def configure(self):
        self.mayaEnvDir = os.path.abspath(self.mayaEnvTemplateDir+"_workingcopy")

        if self.isWindows:
            self.mayaPath = os.path.dirname(self.mayaExecutable)

        self.mayaUserDir = self.mayaEnvDir+"/2015-x64"
        self.mayaModulesDir = os.path.join(self.mayaUserDir,"modules")
        self.mayaShelvesDir = self.mayaUserDir+"/prefs/shelves"
        
    def parseCommandLine(self):
        from optparse import OptionParser
        parser = OptionParser()
        parser.add_option("-m", "--mode", dest="mode",
                          help="maya mode (test, production)")
    
        self.options,_ = parser.parse_args()
        
        if self.options.mode is None:
            self.options.mode = 'test'
            
    def createEnvDir(self):
        if os.path.exists(self.mayaEnvDir):
            shutil.rmtree(self.mayaEnvDir,ignore_errors=False)
        shutil.copytree(self.mayaEnvTemplateDir, self.mayaEnvDir)
        
        scriptsDir = self.mayaEnvDir+'/scripts'
        if not os.path.exists(scriptsDir):
            os.makedirs(scriptsDir)
        
        shutil.copy2(os.path.dirname(__file__)+'/userSetup.py', scriptsDir)
        
    def launch(self):
        self.configure()
        
        env = os.environ.copy()
        env['MAYA_APP_DIR'] = self.mayaEnvDir
        if self.mayaPath is not None:
            env['MAYA_LOCATION'] = self.mayaPath
            env['PATH'] = self.mayaPath
        
        env.pop('PYTHONPATH',None)
        env.pop('PYTHONHOME',None)
        env.pop('PYTHONIOENCODING',None)
        env.pop('PYTHONUNBUFFERED',None)
        
        
        
        self.createEnvDir()
        
        env['maya_test_pythonpath'] = ';'.join(self.pythonPath)
            
        options ={'env':env}
        if self.mayaPath is not None:
            options['cwd'] = self.mayaPath

        print "starting Maya with options:"
        print "python path:",self.pythonPath      
        print "environment template:",self.mayaEnvTemplateDir  
        print "launch mode:",self.options.mode    
        
        commandLine = [self.mayaExecutable,'-nosplash']
        if self.isLinux:
            commandLine = ["/bin/csh","-f"]+commandLine
        print "command line:"," ".join(commandLine)
        
        subprocess.Popen(commandLine,**options).communicate()
