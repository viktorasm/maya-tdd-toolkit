'''
launch maya with settings that will enable launching tests with provided scripts;
feedbacks all stdout output back to IDE
'''
import subprocess
import os
import shutil

import platform
import dccautomation

class Launcher:
    def __init__(self):
        self.mayaExecutable='maya'
        self.mayaPath = None
        self.projectDir = os.path.abspath(os.path.dirname(__file__)+"/..")
        self.mayaEnvTemplateDir = self.projectDir+'/testMayaLaunchEnvironment_snapshot'
        self.projectWorkspace = os.path.abspath(os.path.dirname(__file__)+"/../../")
        
        self.isWindows = 'windows' in platform.system().lower()
            
        # add dcc automation
        self.pythonPath = []
        self.pythonPath.append(os.path.abspath(os.path.dirname(dccautomation.__file__)+"/.."))
        # add self to path
        self.pythonPath.append(self.projectDir)
        
        self.parseCommandLine()
            
    def configure(self):
        self.mayaEnvDir = self.mayaEnvTemplateDir+"_workingcopy"

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
        shutil.rmtree(self.mayaEnvDir,ignore_errors=True)
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
        
        
        
        self.createEnvDir()
        
        env['maya_test_pythonpath'] = ';'.join(self.pythonPath)
            
        options ={'env':env}
        if self.mayaPath is not None:
            options['cwd'] = self.mayaPath

        print "starting Maya with options:"
        print "python path:",self.pythonPath      
        print "environment template:",self.mayaEnvTemplateDir  
        print "launch mode:",self.options.mode    
        
        subprocess.Popen([self.mayaExecutable,'-nosplash'],**options).communicate()
