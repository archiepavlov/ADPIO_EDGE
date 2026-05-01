from typing import Optional
from datetime import datetime
from pony.orm import *

#User, Logs, APP data, f blocks and widgets

def user_rec(db):
    table = 'user_model'

    fields = {
		'_table_': table,

		#'id'         :      PrimaryKey(int, auto = True),

        'name'        :      PrimaryKey( str, 12,  default = 'User',                ),
        'password'    :      Optional  ( str, 16,  default = '',                    ),

        'sessionkey'  :      Optional  ( str, 32,  default = 'No Key',              ), #Unique Seesion ID
        'sessionexp'  :      Optional  ( datetime, default = datetime.now           ), #Expiration Date
        
        'homepage'    :      Optional  ( str, 24,  default = '/system/about',       ),
        'profile'     :      Optional  ( str, 16,  default = 'admin',               ),
        'description' :      Optional  ( str, 64,  default = '',                    ),
    }    
    return type(table.capitalize(),(db.Entity,),fields)
    
#def logger_rec(db):
#    table = 'logger_model'
#
#    fields = {
#		'_table_': table,
#
#		#'id': 	PrimaryKey(int, auto = True),
#        'date':             PrimaryKey(datetime,    default = datetime.now), #precision=0
#		'type':             Optional  (str, 12 ,    default = ''),       
#
#        'text':             Optional  (str, 4096,   default = 'notext'),
#    }
#    return type(table.capitalize(),(db.Entity,),fields)



# Create your models here.
def logic_palette_rec(db):  
    table = 'logic_palette_model'    
    
    fields = {
		'_table_': table,
  
		'id'            :       PrimaryKey( str, 64,  default = 'Funck BLK',                ),
  
        'name'          :       Required ( str, 32,   default = 'name here',                 ),
        'description'   :       Optional ( str, 64,  default = 'description'                ),
        'group'         :       Optional ( str, 24,   default = 'New Group'                  ),
        
        'libimport'     :       Optional ( str, 128,  default = ''                           ),
        'type'          :       Optional ( str, 16,   default = 'block'                      ),

        'function'      :       Optional ( str, 128,  default = 'print(\'Empty Call\')'      ),

        'io'            :       Optional ( Json,      default = []                           ),
    }
    
    return type(table.capitalize(),(db.Entity,),fields)


def graph_palette_rec(db):   
    table = 'graph_palette_model'
    
    fields = {
        '_table_': table,
        
        'id'            : PrimaryKey(int, auto = True),
        
        'name'          : Required ( str, 32,   default = 'name here'   ,                 ),
        'description'   : Optional ( str, 64,   default = 'description'                   ),
        'group'         : Required ( str, 32,   default = 'New Group'                     ),
        
        #'body'          : Required  ( str, 512,  default = '<div>Palette Element:</div>'  ),
        #'widget_area'     : Optional ( str, 32,   default = 'widget_area'                ),
        
        #'properties'    : Optional  ( Json, default = []                                  ),
    }
    
    return type(table.capitalize(),(db.Entity,),fields)



    