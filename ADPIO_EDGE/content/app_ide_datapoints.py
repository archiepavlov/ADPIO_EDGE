from pony.orm import *
import ujson

#DB
from database.app_db    import find_app_db

from assets.dataconversion import  str_to_dp
from content.users import check_permissions


def to_json(rec, app_status):
    group = rec.group
    if group == '':
        group = 'No Group'
    
    return {
        "id"                : rec.id, 
        "name"              : rec.name, 
        "description"       : rec.description, 
        "group"             : group,          
                
        "datatype"          : rec.datatype, 
        "value"             : str_to_dp(rec.value, rec.datatype),
        "units"             : rec.units,
        "writable"          : rec.writable, 
        
        "memalloc"          : rec.memalloc,

        "properties"        : rec.properties,
        "protocol"          : rec.protocol,
        "trend"             : rec.trend,
    }


async def update(db, content):
    with db_session: #db.graphics.select().order_by(lambda r: r.order)
        return [ to_json(rec, content["app_status"]) for rec in db.datapoints.select()]#.order_by(lambda r: r.group) ]
               
    return []
        

async def get_dataponts(db, content):
    try:
        with db_session:
            return [ to_json(rec, False) for rec in db.datapoints.select() ]        
    except:
        return  {"result": "error", "error_text": "Failed To Obtain Datapoint"}    


async def add_datapoint(db, content):
    try:
        with db_session:
            for rec in content["datapoints"]:
                db.datapoints (
                    name         = rec['name'] ,
                    description  = rec['description'],

                    datatype     = rec['datatype'],
                    value        = str(rec['value']),
                    units        = rec['units'],
                    writable     = rec['writable'],

                    group        = rec['group'], 

                    properties   = rec['properties'], 
                    protocol     = rec['protocol'], 
                    trend        = rec['trend'],                                                 
                )

                rec = db.datapoints.select().order_by(desc(db.datapoints.id)).limit(1)[0]

                    #return  {"result": "ok", "datapoint": to_json(rec, False)}
            
    except Exception as ex:
        print("Failed To Add New Point" + str(ex))
        #return  {"result": "error", "error_text": f"Failed to add new datapoint: {str(ex)}"}

    return  [ to_json(rec, False) for rec in db.datapoints.select()]        
         
async def delete_datapoint(db, content):
    try:
        for rec in content["datapoints"]:
            with db_session:
                db.datapoints[rec['id']].delete()

        return  [ to_json(rec, False) for rec in db.datapoints.select()]
            
    except Exception as ex:
        return  {"result": "error", "error_text": "Failed to delete datapoint "}

async def save_datapoint(db, content):
    try:
        with db_session:
            for rec in content["datapoints"]:           
                data_point = db.datapoints[rec['id']]
                    
                data_point.name            = rec['name']
                data_point.description     = rec['description']

                data_point.datatype        = rec['datatype']
                data_point.value           = str(rec['value'])
                data_point.units           = rec['units']
                data_point.writable        = rec['writable']

                #data_point.memalloc        =   rec['memalloc']
                data_point.group           = rec['group']
                        
                data_point.properties      = rec['properties']
                data_point.protocol        = rec['protocol']
                data_point.trend           = rec['trend']
                
        return  [ to_json(rec, False) for rec in db.datapoints.select()]
    except Exception as ex:
        return  {"result": "error", "error_text": "Failed to save datapoint "}


def load_datapoints(app_name):    
    db = find_app_db(app_name)

    with db_session:
        return [ to_json(rec, False) for rec in db.datapoints.select() ]


def save_mem_alloc(app_name, datapoints):    
    db = find_app_db(app_name)

    mem_alloc = 3 #Starts from 3
    for dp in datapoints:
        with db_session:
            data_point          = db.datapoints[dp['id']]
            data_point.memalloc = mem_alloc
            dp['memalloc']      = mem_alloc
        
        mem_alloc += 1

    return datapoints    



COMMANDS_DICT = {
    'update'            : update            ,  'perm_update'           : 'developer, user, view, ',
    'get_dataponts'     : get_dataponts     ,  'perm_get_dataponts'    : 'developer, user, view, ',
    'add_datapoint'     : add_datapoint     ,  'perm_add_datapoint'    : 'developer, ',
    'delete_datapoint'  : delete_datapoint  ,  'perm_delete_datapoint' : 'developer, ',
    'save_datapoint'    : save_datapoint    ,  'perm_save_datapoint'   : 'developer, ',
}

#DEFAULT
async def default_msg(content):
    print('Request Error app_ide_datapoints_mng: ' + str(content))
    return {"result": "error", "error_text": "app_ide_datapoints_mng command not found"}

async def app_ide_datapoints_mng(auth, cmd, content):
    content_json = ujson.loads( content )
    app_db = find_app_db(content_json["name"])

    if check_permissions(auth, COMMANDS_DICT['perm_' + cmd]):
        return await COMMANDS_DICT.get(cmd, default_msg)(app_db, content_json)
    else:
        return { "result": "error", "error_text": f"Permission denied for user '{auth['user']}' accessing '{cmd}'" }
