from pony.orm import *

from system.globals import WORKSPACE

from database.model_app     import app_rec
from database.model_system  import logger_rec, user_rec, graph_palette_rec, logic_palette_rec


class __db_serv:
    def __init__(self):
        self.dbase = None
        
        self.apps                = None

        self.users               = None
        self.logger              = None

        self.grpah_palette       = None
        self.logic_palette       = None
        

    def init_db(self):            
        self.dbase = Database()
        #sql_debug(True)
        self.dbase.bind("sqlite", f"{WORKSPACE}/db.sqlite", create_db = True)
        
        self.apps                = app_rec(self.dbase)

        self.users               = user_rec   (self.dbase)
        self.logger              = logger_rec (self.dbase)

        self.grpah_palette       = graph_palette_rec(self.dbase)
        self.logic_palette       = logic_palette_rec(self.dbase)

        self.dbase.generate_mapping(create_tables = True)

        if __debug__:
            print("Data Base Initilized")        
        
        
    def close_db(self):
        self.dbase.disconnect()
        
        
db  = __db_serv()