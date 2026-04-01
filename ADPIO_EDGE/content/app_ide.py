from pony.orm import *

import ujson
import os
from shutil import rmtree

#settings
from system.globals import APPS_FOLDER

#DB
from database.db_main import db
from database.app_db    import create_app_db, delete_app_db

#app exec
from system.app_engine import build_app, run_app, stop_app, get_app_status


from content.users import check_permissions


async def to_json(rec):
    try:
        status, loop = await get_app_status( rec.name ) 
    except:
        status = False 
        loop = -1

    res = {
        "status"      :   status,
        "name"        :   rec.name,
        "group"       :   rec.group,
        "description" :   rec.description,
        "version"     :   rec.version,
        "autostart"   :   rec.autostart,
    }

    return res


def get_app_json(app, status):
    with db_session:
        app_r = db.apps[ app['name'] ]

        return  {
            "name"         : app_r.name ,
            "description"  : app_r.description ,
            "group"        : app_r.group ,
            "version"      : app_r.version ,
            "status"       : status,
            "autostart"    : app_r.autostart ,
            "t_created"    : str(app_r.t_created),
            "t_updated"    : str(app_r.t_updated),
            "t_built"      : str(app_r.t_built),

            "view_list"    : app_r.view_list,
            "selected_view": app_r.view_list[0]['value'] #Set Default View                 
        }


async def update_list(content):            
    with db_session: 
        return [ await to_json(rec) for rec in db.apps.select() ]
        
    return []


async def get_app(content):
    try:
        status, loop = await get_app_status( content['name'] ) 
    except:
        status = False 
        loop = -1

    try:
        return get_app_json(content, status)
    except:
        return  {"result": "error", "error_text": "Failed to obtain app data"}            
            
            
async def add_app(content):
    try:
        with db_session:
            db.apps (
                name         = content['name'] ,
                description  = content['description'] ,
                group        = content['group'] ,
                version      = content['version'] ,
                autostart    = content['autostart']
                #t_created    = str(content.t_created),
                #t_updated    = str(content.t_updated),
                #t_built      = str(content.t_built),                           
            )
    
        if ( not os.path.isdir(f"{APPS_FOLDER}/{content['name']}" )):
            try: 
                os.mkdir(f"{APPS_FOLDER}/{content['name']}")
            except OSError as error:  
                print(error)
        
        create_app_db(content['name'])

        return  {"result": "ok"}
    except Exception as ex:
        print(str(ex))
        return  {"result": "error", "error_text": f"Failed to add new app (Name should be unique, {ex})"}


async def save_app(content):
    try:
        with db_session:
            for rec in content: 
                app_s = db.apps[ rec['name'] ]

                app_s.name         = rec['name']
                app_s.description  = rec['description']
                app_s.group        = rec['group']
                app_s.version      = rec['version']
                app_s.autostart    = rec['autostart']
                #t_created    = str(content.t_created),
                #t_updated    = str(content.t_updated),
                #t_built      = str(content.t_built),                   
        
        return  {"result": "ok"}
    except  Exception as ex:
        print(str(ex))
        return  {"result": "error", "error_text": f"Failed to save app... ({ex})"}


async def delete_app(content): 
    try:
        delete_app_db(content['name'])
        
        with db_session:
            db.apps[content['name']].delete()

        if (os.path.isdir(f'{APPS_FOLDER}/{content['name']}')):
            try: 
                await stop_app(content['name'])
            except OSError as error:  
                print(error)

        try: 
            rmtree(f'{APPS_FOLDER}/{content['name']}')
        except OSError as error:  
            print(error)            
            
        return  {"result": "ok"} 
    except  Exception as ex:
        print(str(ex))
        return  {"result": "error", "error_text": f"Failed to delete app ({ex})"}


async def add_view(content):
    try:
        with db_session:
            app_r = db.apps[ content['name'] ]

            for rec in app_r.view_list:
                if rec['value'] == content['view']:
                    return  {"result": "error", "error_text": "View already exists"}

            app_r.view_list.append( {'name': content['view'], 'value': content['view']} )
                   
        return get_app_json(content, False)
    except:            
        return  {"result": "error", "error_text": "Failed to add new view"}


async def delete_view(content):
    try:
        with db_session:
            app_r = db.apps[ content['name'] ]
    
            if len(app_r.view_list) == 1:
                return  {"result": "error", "error_text": "At least one view should exist "}

            for rec in app_r.view_list:
                if rec['value'] == content['view']:
                    app_r.view_list.remove(rec)
                    break

        return get_app_json(content, False)
    except:                
        return  {"result": "error", "error_text": "Failed to delete view"}


async def app_status(content):
    try:
        status, loop = await get_app_status(content['name'])  #loop_cnt/{loop_cnt
        print(f"{content['name']} Status/Loop: {status}/{loop}")
    except:
        print(f'App {content['name']} Offline')
    

    return { 'result': 'ok', }


async def build_apk(content):     
    await build_app(content['name'])
    return { 'result': 'ok', }


async def run_apk(content):
    return await run_app(content['name'])
    
        
async def stop_apk(content):
    try:
        await stop_app(content['name'])
    except:
        print(f'App {content['name']} Already Stopped')  
        return {"result": "error", "error_text": f'App already stopped: {content['name']}'}
            
    return { 'result': 'ok', } 


COMMANDS_DICT = {
    'update_list'   :  update_list  , 'perm_update_list'  : 'developer, ',
    'get_app'       :  get_app      , 'perm_get_app'      : 'developer, ',
    'add_app'       :  add_app      , 'perm_add_app'      : 'developer, ',
    'save_app'      :  save_app     , 'perm_save_app'     : 'developer, ',
    'delete_app'    :  delete_app   , 'perm_delete_app'   : 'developer, ',
    'add_view'      :  add_view     , 'perm_add_view'     : 'developer, ',
    'delete_view'   :  delete_view  , 'perm_delete_view'  : 'developer, ',
    'app_status'    :  app_status   , 'perm_app_status'   : 'developer, user, view, ',
    'build_app'     :  build_apk    , 'perm_build_app'    : 'developer, ',
    'run_app'       :  run_apk      , 'perm_run_app'      : 'developer, ',
    'stop_app'      :  stop_apk     , 'perm_stop_app'     : 'developer, ',
}


#DEFAULT
async def default_msg(content):
    print('Request Error app_ide_mng: ' + str(content))
    return {"result": "error", "error_text": "app_ide_mng command not found"}

async def app_ide_mng(auth, cmd, content):
    content_json = ujson.loads( content )

    if check_permissions(auth, COMMANDS_DICT['perm_' + cmd]):
        return await COMMANDS_DICT.get(cmd, default_msg)(content_json)
    else:
        return { "result": "error", "error_text": f"Permission denied for user '{auth['user']}' accessing '{cmd}'" }
