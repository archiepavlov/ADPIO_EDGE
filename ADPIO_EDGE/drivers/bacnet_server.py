import threading
import ujson
import asyncio

from content.logger    import print_log_bacnet
from system.shared_mem import get_server_mem, server_mem_name, BCNT_DB_MEM_ADDR, BCNT_CMD_MEM_ADDR

from bacpypes3.debugging import bacpypes_debugging, ModuleLogger
from bacpypes3.argparse import SimpleArgumentParser
from bacpypes3.app import Application
from bacpypes3.pdu import Address, LocalBroadcast, RemoteBroadcast, GlobalBroadcast
from bacpypes3.primitivedata import Unsigned, ObjectIdentifier, PropertyIdentifier
from bacpypes3.errors import MissingRequiredParameter
from bacpypes3.constructeddata import AnyAtomic
from bacpypes3.apdu import ErrorRejectAbortNack

#import bacpypes3.object import AnalogValueObject
#import bacpypes3.object as _client_object

#from bacpypes3.object        import Object as _client_object
#from bacpypes3.local.object  import Object as _server_object



class bacnet_server():
    def __init__(self, *args):
        self.thrd = None
        self.debug           = False
        self.tasks           = []
        self.task_mng_sleep  = 1

        self.status          = False #status
        self.bacnet_app      = None
        self.settings        = []

        self.who_is_onstart  = False

        self.CMDS_DICT = {
            'who_is'                 : self.who_is,                 #low_limit = 0, high_limit = 4194303
            'clear_db'               : self.clear_db,             
            'read_property'          : self.read_property,   
            'read_property_multi'    : self.read_property_multi, 
            'read_device_list'       : self.read_device_list,       #Register in db
            'read_property_multi_db' : self.read_property_multi_db, #Register in db
            
            'write_property'         : self.write_property, 
        }       


    async def init_service(self, settings_adapter):
        #Set general settings
        self.task_mng_sleep = settings_adapter['task_mng_sleep']
        self.debug          = settings_adapter['debug']
        self.who_is_onstart = settings_adapter['debug']

        #Set adapter's settings
        settings_adapter['server'][0][1]["bacnet-ip-udp-port"] = settings_adapter['bip_port']
        settings_adapter['server'][0][1]["ip-address" ]        = settings_adapter['bip_ip']
        settings_adapter['server'][0][1]["ip-subnet-mask"]     = settings_adapter['bip_mask']
        settings_adapter['server'][0][1]["mac-address"]        = f"{settings_adapter['bip_ip']}:{settings_adapter['bip_port']}"

        self.settings = settings_adapter['server'][0]

        self.thrd = threading.Thread(target=self.run_service, args=())
        self.thrd.start()        


    def run_service(self):
        asyncio.run( self.run_async_service(self.settings) )


    async def run_async_service(self, settings):
        #TEST av
        #av = AnalogValueObject(
        #    objectIdentifier=("analogValue", 0),
        #    objectName="Test AV",
        #    presentValue=-1,
        #    covIncrement=0.5,
        #)
       
        await print_log_bacnet(f"BACnet Service Started: {settings[1]["mac-address"]}, {settings[0]["object-identifier"]}")

        #build BACnet application        
        self.bacnet_app = Application.from_json(settings)
        #self.bacnet_app.add_object( av )
        
        self.bacnet_app.i_am()

        self.status = True
        
        if self.who_is_onstart: await self.add_task('who_is', {})

        while self.status:  #BACnet task manager Loop
            try: 
                if (len(self.tasks) > 0):
                    if self.debug:
                        print("BACnet: Tasks Left: ",  len(self.tasks), '\n')
                        print(f"BACnet: Executing Command: {self.tasks[0]}")

                    await self.CMDS_DICT.get(self.tasks[0]['cmd'], self.cmd_error)(self.tasks[0]['params']) #default_msg

            except ErrorRejectAbortNack as ex:
                print(f"Err1, BACnet: {ex}")
            except Exception as ex:  
                print(f"Err10, BACnet: {ex}")
            except OSError as ex:
                print(f"Err11, BACnet: {ex}") 
            except:
                print(f"Err12, BACnet: Unknown error")
            finally:
                if (len(self.tasks) > 0):
                    self.tasks.pop(0)
              
                new_tsk = get_tasks()
                set_tasks([])

                if (len(new_tsk) > 0):
                    for tsk in new_tsk:
                        if tsk not in self.tasks:
                            self.tasks.append(tsk)
                        else:
                            if self.debug: print(f"New Task Rejected, Already exists")
                            
            await asyncio.sleep(self.task_mng_sleep) 

        self.bacnet_app.close()
        await print_log_bacnet("BACnet Service Terminated")


    def terminate_service(self):
        self.status = False
        self.tasks  = []


    async def clear_db(self, params):
        self.tasks  = []
        set_devices  ([])
        

    async def add_task(self, cmd, params):
        self.tasks.append({'cmd': cmd, 'params': params})


    async def add_tasks(self, cmds):
        self.tasks.extend(cmds) #add list [{cmd, params}, ...]


    async def who_is(self, params): #//low_limit = 0, high_limit = 4194303
        if 'low_limit' in params and 'high_limit' in params:
            low_limit  = params['low_limit']
            high_limit = params['high_limit']
        else:
            low_limit = 0
            high_limit = 4194303
            
        i_ams = await self.bacnet_app.who_is(low_limit, high_limit)

        devices = get_devices()

        for i_am in i_ams:  
            device_instance = i_am.iAmDeviceIdentifier[1]
            device_address  = i_am.pduSource

            if self.debug:
                print(f"BACnet who_is device found: {device_instance} - {device_address}")

            device = find_device(devices, device_address)

            net         = str(device_address)
            name        = ""
            description = ""
            location    = ""
            list_size   = 0

            segment_rx  = False
            segment_tx  = False

            
            #Get Device Info
            try:    name = await self.read_property({'net': net, 'object': f'device, {device_instance}', 'property': 'object-name'})
            except: print(f"Failed to get device {device_address} name")

            try:    description = await self.read_property({'net': net, 'object': f'device, {device_instance}', 'property': 'description'})
            except: print(f"Failed to get device {device_address} desciption")
            
            try:    location = await self.read_property({'net': net, 'object': f'device, {device_instance}', 'property': 'location'})
            except: print(f"Failed to get device {device_address} location")

            try:    
                segment = await self.read_property({'net': net, 'object': f'device, {device_instance}', 'property': 'segmentation-supported'})
                match segment:
                    case 0:
                        segment_rx  = True
                        segment_tx  = True
                    case 1:
                        segment_rx  = False
                        segment_tx  = True
                    case 2:
                        segment_rx  = True
                        segment_tx  = False
                    case 3:
                        segment_rx  = False
                        segment_tx  = False

            except: print(f"Failed to get device {device_address} segmentation")            

            try:    list_size = await self.read_property({'net': net, 'object': f'device, {device_instance}', 'property': 'object-list', 'index': 0})
            except: print(f"Failed to get device {device_address} list_size")                        

            if device == None:
                devices.append({
                    "id"            : len(devices),
                    "device_id"     : device_instance,
                    "net"           : str(device_address),
                    "name"          : name,
                    "description"   : description,
                    "location"      : location,
                    "segment_rx"    : segment_rx,
                    "segment_tx"    : segment_tx,
                    "list_size"     : list_size,
                    "objects"       : [],
                })

                if self.debug:
                    print(f"New Device Added! : {device_instance} - {device_address}")     

        set_devices(devices)


    async def read_property(self, params): #net, obj type, obj id, array opt
        #params = {'id': 0, 'net': '192.168.1.160:47808', 'object': 'analog-input, 12', 'property': 'presentValue', 'index': 0}

        device_net  = Address           (params["net"])
        object      = ObjectIdentifier  (params["object"])
        property    = PropertyIdentifier(params["property"])
        
        array_index = None
        if 'index' in params:
            array_index = params["index"]
        
        value = await self.bacnet_app.read_property(device_net, object, property, array_index = array_index )   
        
        if self.debug:
            print(f"Property Read: {device_net}: {object}, {property} = {value}")

        return value



    async def read_property_multi(self, params): #Register object/property in database
        #'cmd': 'read_property_multi_db', 
        #'params': { 
        #    'id'        : device.id, 
        #    'net'       : device.net,  
        #    'requests'  : [
        #    'analog-input, 1', ['presentValue', 'objectName'],
        #    'analog-input, 2', ['presentValue']
        #    ]          
        #}         
   
        values = await self.bacnet_app.read_property_multiple(params["net"], params["requests"])

        if __debug__:
            for obj in values:
                print(f'multi req obj/prp: {obj[0]} / {obj[1]} [{obj[2]}] = {obj[3]}')
        
        return values



    async def read_device_list(self, params): #Register object/property in database
        #'cmd': 'read_device_list', 
        #'params': {
        #    'id'        : 0,  -device index
        #    'net'       : device.net, - net
        #    'object'    : `device, 1`, - object
        #    'property'  : 'prop',  - prop
        #    'index'     : i  - optional index
        #}

        devices = get_devices()        
        device  = devices[params['id']]

        if device["net"] != params["net"]:
            print_log_bacnet(f"MSG Dismissed: mismatch id vs device net {device["net"]} !== {params["net"]}")
            pass

        obj_list = await self.read_property(params) #ObjectIdentifier Type

        if not isinstance(obj_list, list): #Fix for no segmentation calls
            obj_list = [obj_list]

        if params['property'] == 'object-list': #Check for new objects
            for obj in obj_list:         
                object = find_object(device, obj)

                if object == None:
                    device['objects'].append({
                        "object_id"  : len(device['objects']),
                        "object"     : str(obj),
                        "name"       : "",
                        "value"      : "", 
                        "properties" : [], #name, datatype, value
                    })

                    if self.debug: print(f"{device["net"]}: New object {len(device['objects'])}: {obj}")

            set_devices(devices)



    async def read_property_multi_db(self, params): #Register object/property in database
        devices = get_devices()  

        device  = devices[params['id']]
        if device["net"] != params["net"]:
            print_log_bacnet(f"MSG Dismissed: mismatch id vs device net {device["net"]} !== {params["net"]}")
            pass

        respond = await self.read_property_multi(params)
    
        for resp in respond:
            #0 - object, 1 - prop, 2 - idk, 3 - value  
            object   = find_object  (device, resp[0])
            property = find_property(object, resp[1])            
            value = str(resp[3])

            if property == None:
                object['properties'].append({
                    "property"     : str(resp[1]),
                    "value"        : value, 
                })
            else:
                property['value'] = value

            match str(resp[1]):
                case "object-name":   object["name" ] = value
                case "present-value": object["value"] = value                

        set_devices(devices)


    async def write_property(self, params):
        # device_address,  object_identifier,  property_identifier,
        # value, property_array_index,  priority,

        device_net  = Address           (params["net"])
        object      = ObjectIdentifier  (params["object"])
        property    = PropertyIdentifier(params["property"])
        value       = params["value"]
        priority    = params["priority"]
        
        array_index = None
        if 'index' in params:
            array_index = params["index"]
        
        await self.bacnet_app.write_property(device_net, object, property, value, array_index=array_index, priority=priority )   
        
        if self.debug:
            print(f"Property Write: {device_net}: {object}, {property} = new value {value}")

        return {"result": "OK"}


    async def cmd_error(self, params):
        print(f'BACnet CMD Error: not found {params}')
        return {"result": "error", "error_text": "app_ide_mng command not found"}        
    


def set_devices(devices_jsn):
    SERVER_MEM =  get_server_mem()
    SERVER_MEM[BCNT_DB_MEM_ADDR] = ujson.dumps( devices_jsn ) 


def get_devices():
    return ujson.loads( get_server_mem()[BCNT_DB_MEM_ADDR] )


def set_tasks(cmnds_jsn):
    SERVER_MEM =  get_server_mem()
    SERVER_MEM[BCNT_CMD_MEM_ADDR] = ujson.dumps( cmnds_jsn ) 


def add_new_tasks(cmnds_jsn):
    new_tasks = get_tasks()
    new_tasks.extend(cmnds_jsn)

    SERVER_MEM = get_server_mem()
    SERVER_MEM[BCNT_CMD_MEM_ADDR] = ujson.dumps( new_tasks )     


def get_tasks():
    return ujson.loads( get_server_mem()[BCNT_CMD_MEM_ADDR] )


def find_device(devices, device_net):
    for dev in devices:
        if  device_net == dev['net']:
            return devices
        
    return None


def find_object(device, object):
    searched = str(object)
    for obj in device['objects']:
        if obj['object'] == searched:
            return obj
        
    return None


def find_property(object, property):
    searched = str(property)
    for prp in object['properties']:
        if prp['property'] == searched:
            return prp
        
    return None