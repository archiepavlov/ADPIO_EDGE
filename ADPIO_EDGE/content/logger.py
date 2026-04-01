from pony.orm import *
import ujson
 
#DB
from database.db_main import db

from content.users import check_permissions


def to_json(rec):
    return {
        "date": str(rec.date).split('.')[0], 
        "type": rec.type,                    
        "text": rec.text,                    
    }


async def update(content):
    with db_session: 
        return [ to_json(rec) for rec in db.logger.select().order_by(desc(db.logger.date)).limit(128) ]
        
    return []


async def clear_all(content):
    with db_session: 
        db.logger.select().delete(bulk = True)
        
    return { "result": "ok", } 


async def print_log_system(txt):
    """global last_records_info

    if txt not in last_records_info:
        last_records_info.insert(0, txt)
        if len( last_records_info ) > __max_back_log:
            last_records_info.pop(__max_back_log)
    """

    txt_trim = txt
    if (len(txt) > 2018):
        txt_trim = txt[:2018] + '...'

    with db_session:
        db.logger (type='system', text=txt_trim)
    
    print( f'System: {txt}' )
    return {'system' : txt}


async def print_log_error(txt):
    """global last_records_error

    if txt not in last_records_error:
        last_records_error.insert(0, txt)
        if len( last_records_error ) > __max_back_log:
            last_records_error.pop(__max_back_log)
    """

    txt_trim = txt
    if (len(txt) > 2018):
        txt_trim = txt[:2018] + '...'

    with db_session:
        db.logger (type='error', text=txt_trim)
    
    print( f'Error: {txt}' )
    return {'error' : txt}


async def print_log_lora(txt):
    """global last_records_info

    if txt not in last_records_info:
        last_records_info.insert(0, txt)
        if len( last_records_info ) > __max_back_log:
            last_records_info.pop(__max_back_log)
            
    """
    
    txt_trim = txt
    if (len(txt) > 2018):
        txt_trim = txt[:2018] + '...'

    with db_session:
        db.logger (type='loraWAN', text=txt_trim)
    
    print( f'loraWAN: {txt}' )
    return {'loraWAN' : txt}


async def print_app_event(txt):
    txt_trim = txt
    if (len(txt) > 2018):
        txt_trim = txt[:2018] + '...'

    with db_session:
        db.logger (type='APPS', text=txt_trim)
    
    print( f'APPS: {txt}' )
    return {'APPS' : txt}


async def show_logs(content):
    filename = f'/dev/shm/adpio_{content['file']}.log'

    content = []
    max_size = 256
    try:
        with open(filename, 'r') as f:
            #content = f.readlines()
            for line in f:
                content.append( line.replace('\n', '') )

            if len(content) > max_size:
                content = content[(len(content) - max_size):len(content)]

    except FileNotFoundError:
        return { 'content': content }
        

    return { 'content': content }
            

async def clear_logs(content):
    filename = f'/dev/shm/adpio_{content['file']}.log'

    try:
        with open(filename, 'w') as f:
          return {'content': ''}
    except FileNotFoundError:
        print(f"Error: The file 'adpio_{content['file']}.log' was not found.")


COMMANDS_DICT = {
    'update'    : update,    'perm_update'       : 'developer, user, view, ', #Note: This on is DB records, controled by server
    'clear_all' : clear_all, 'perm_clear_all'    : 'developer, ',

    'show_logs' : show_logs,  'perm_show_logs'   : 'developer, ',             #Logs from console, python errors
    'clear_logs': clear_logs, 'perm_clear_logs'  : 'developer, ',
}


#DEFAULT
async def default_msg(content):
    print('Request Error log_task_mng: ' + str(content))
    return {"result": "error", "error_text": "log_task_mng command not found"}


async def log_task_mng(auth, cmd, content):
    content_json = ujson.loads( content )

    if check_permissions(auth, COMMANDS_DICT['perm_' + cmd]):
        return await COMMANDS_DICT.get(cmd, default_msg)(content_json)
    else:
        return { "result": "error", "error_text": f"Permission denied for user '{auth['user']}' accessing '{cmd}'" }
