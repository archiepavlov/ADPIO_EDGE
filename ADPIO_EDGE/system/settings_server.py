import ujson
import os
import shutil
from system.globals import ROOT_FOLDER, WORKSPACE, APPS_FOLDER, ASSET_FOLDER

class settings_cfg:
    def __init__(self):
        self.uvicorn        = None
        self.loraWAN_server = None

        self.python       = ''
        self.terminal     = False
        
        self.create_work_folder()        
        
    def create_work_folder(self):
        #make workspace
        if (not os.path.isdir(WORKSPACE)):
            try: 
                os.mkdir(WORKSPACE)
            except OSError as error:  
                print(error)
                
        #make default setings file
        if (not os.path.isfile(f'{WORKSPACE}/settings.json')):
            try: 
                shutil.copy2( f'{ROOT_FOLDER}/assets/settings.json', f'{WORKSPACE}/settings.json' )
            except OSError as error:  
                print(error)

        #make apps folder
        if (not os.path.isdir(APPS_FOLDER)):
            try: 
                os.mkdir(APPS_FOLDER)
            except OSError as error:  
                print(error)
        
        #make assets folder
        if (not os.path.isdir(ASSET_FOLDER)):
            try: 
                os.mkdir(ASSET_FOLDER)
            except OSError as error:  
                print(error)      

        #LOGS - HDD
        if (not os.path.isdir(WORKSPACE + '/log')):
            try: 
                os.mkdir(WORKSPACE + '/log')
            except OSError as error:  
                print(error)      
        
        
                                      

        """if (not os.path.isdir(ASSET_FOLDER)):
            try: 
                os.mkdir(ASSET_FOLDER)
            except OSError as error:  
                print(error)

        if (not os.path.isdir(BUILD_FOLDER)):
            try: 
                os.mkdir(BUILD_FOLDER)
            except OSError as error:  
                print(error)

        if (not os.path.isfile(WORK_FOLDER + '/settings.json')):
            try: 
                if __debug__:
                    shutil.copy2( ROOT_FOLDER + '/assets/settings_dev.json', WORK_FOLDER + '/settings.json')
                else:
                    shutil.copy2( ROOT_FOLDER + '/assets/settings.json', WORK_FOLDER + '/settings.json')
            except OSError as error:  
                print(error)           
        """
        
    def read_settings(self):
        with open (f'{WORKSPACE}/settings.json' ) as f:
            rd = f.read()
            cls = ujson.loads( rd )
            
            self.python         = cls['python_exe']
            self.terminal       = cls['terminal']
            
            self.uvicorn        = cls['uvicorn']
            self.loraWAN_server = cls['loraWAN_server']

    """
    def write_settings(self):
        jsn = {
            'uvicorn':         self.uvicorn,
            'app_ids':         self.app_ids,
            'loraWAN':       self.loraWAN,
        }
        with open(WORK_FOLDER + '/settings.json', 'w') as f:
            f.write( ujson.dumps(jsn,  default = lambda o: o.__dict__, indent=4) )
    """