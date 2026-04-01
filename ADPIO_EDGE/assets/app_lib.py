from typing import Optional
from datetime import datetime
from pony.orm import *


#SUB database in app folder
def app_datapoint_rec(db):
    table = 'app_datapoints_model'

    fields = {
		'_table_': table,

		'id'              : PrimaryKey(int, auto = True),

        'name'            : Optional( str, 32,   default = 'Datapoint',                 ),
        'description'     : Optional( str, 128,  default = '',                          ),
        'group'           : Optional( str, 24,   default = '',  nullable=True           ),

        'datatype'        : Optional( str, 8,    default = '',                          ),
        'value'           : Optional( str, 128,  default = '',                          ),
        'writable'        : Optional( bool,      default = True                         ),
        'units'           : Optional( str, 24,   default = '',                          ),

        'memalloc'        : Required( int,       default = 0                            ),

        'properties'      : Optional( Json,      default = [],                          ),
        'protocol'        : Optional( Json,      default = [],                          ),
        'trend'           : Optional( Json,      default = [],                          ),
    }

    return type(table.capitalize(),(db.Entity,),fields)


def app_trend_rec(db):
    table = 'app_trend_model'

    fields = {
		'_table_': table,

		#'id'              : PrimaryKey(int, auto = True                                ),
        #datetime, default = datetime.now, precision=0 
        
        'time'            : PrimaryKey(datetime, auto = True, default = datetime.now,  ),
        'name'            : Required( str, 32,  default = 'Datapoint',                 ),

        'value'           : Required( str, 128, default = '0',                         ),
        'datatype'        : Optional( str, 8,   default = '',                          ),
        
    }

    return type(table.capitalize(),(db.Entity,),fields)


class __app_db_runtime:
    def __init__(self, app_name):
        self.dbase = None
        self.app_name = app_name
        
        self.datapoints      = None
        self.trends          = None


    def init_db(self):  #For IDE Editing
        self.dbase = Database()
        self.dbase.bind("sqlite", f"applications/{self.app_name}/app_db.sqlite", create_db = False)
        
        self.datapoints         = app_datapoint_rec(self.dbase)
        self.trends             = app_trend_rec    (self.dbase)

        self.dbase.generate_mapping(create_tables = False)

        if __debug__:
            print(f"{self.app_name} Data Base Runtime Initilized!")        
        

    def close_db(self):
        self.dbase.disconnect()
        
        if __debug__:
            print(f"APP {self.app_name} Data Base Runtime Terminated...")

