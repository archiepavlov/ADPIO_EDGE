from pony.orm import *
import ujson

#Tools
from drivers.loraWAN_conn_sever import get_loraWAN_db
from drivers.bacnet_server      import get_devices, set_devices, get_tasks, set_tasks, add_new_tasks

from content.users import check_permissions


async def lora_update(content):
    return get_loraWAN_db()
    

async def lora_find_device(content):
    for dev in get_loraWAN_db():
        if dev['devEUI'] == content['devEUI']:
            return dev
        
    return {}


async def bacnet_update(content):
    return get_devices()


async def bacnet_read_properties(content):
    add_new_tasks( content )
    return  { 'result': 'ok', } 


COMMANDS_DICT = {
    'lora_tools_update'            : lora_update,            'perm_lora_tools_update'            : 'developer, ',
    'lora_tools_find_device'       : lora_find_device,       'perm_lora_tools_find_device'       : 'developer, ',

    'bacnet_tools_update'          : bacnet_update,          'perm_bacnet_tools_update'          : 'developer, ',
    'bacnet_tools_read_properties' : bacnet_read_properties, 'perm_bacnet_tools_read_properties' : 'developer, ',
}


#DEFAULT
async def default_msg(content):
    print('Request Error log_task_mng: ' + str(content))
    return {"result": "error", "error_text": "network_tools_task_mng command not found"}


async def network_tools_mng(auth, cmd, content):
    content_json = ujson.loads( content )

    if check_permissions(auth, COMMANDS_DICT['perm_' + cmd]):
        return await COMMANDS_DICT.get(cmd, default_msg)(content_json)
    else:
        return { "result": "error", "error_text": f"Permission denied for user '{auth['user']}' accessing '{cmd}'" }
