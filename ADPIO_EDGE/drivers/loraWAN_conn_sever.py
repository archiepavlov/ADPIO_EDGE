import threading
import socket
import ujson
import asyncio

from assets.dataconversion      import set_mem_value

#Connects loraWAN via http. loraWAN - client - this one is server
from content.logger    import print_log_lora
from system.shared_mem import get_server_mem



class loraWAN_server:
    def __init__(self):
        self.port       = 9002
        self.debug      = False
        self.listen     = 1
        self.settimeout = 8        

        self.status = False

        self.thrd = None
        self.sock = None

        #self.device_db   = []


    async def init_service(self, port, debug, listen, settimeout):
        self.port   = port
        self.debug  = debug

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
            self.sock.bind(('', self.port))  #host, port 
        except socket.error:
            await print_log_lora(f"LoRaWAN HTTP API: Failed to bind socket" )
            return False

        await print_log_lora(f"LoRaWAN HTTP API: port = {self.port}, debug = {self.debug}")
            
        # put the socket into listening mode  (backlog)
        self.sock.listen    (self.listen)
        self.sock.settimeout(self.settimeout)

        self.thrd = threading.Thread(target=self.run_service, args=())
        self.thrd.start()
        
        return True
        

    def run_service(self):
        self.status = True
       
        req_data = ""
        while self.status:
            c_s = None

            try: 
                c_s, addr = self.sock.accept()


                req_data = "" #get loraWAN data
                while True:
                    data = c_s.recv(4096)
                    req_data += str(data, "utf-8") 
                    
                    if (len(data)  < 4096): break #If message shorter, then exit, is it the end
                    if (len(data) == 4096 and req_data[len(req_data) - 1] == '}'): break #Check rear Accurance, when last chunk is the last

                if self.debug:
                    print(f"LoRaWAN Request from addr: {addr}")
                    print(req_data)
                    print()

                req_data = ujson.loads( req_data[req_data.index("{"):] )
                self.mile_database_update(req_data)

                c_s.send( '{"status": "OK"}'.encode() ) #just any return to loraWAN
                c_s.close()        
            except socket.timeout:  
                pass
            except Exception as ex:  
                print(f"Error1, LoRaWAN! Err {ex}, data len {len(data)}, Req: { req_data }") 
                c_s.close()
            except OSError as ex:
                print(f"Error2, LoRaWAN! Err {ex}, data len {len(data)}, Req: { req_data }") 
                c_s.close()
                  

            #Sync Values with app
            asyncio.run( self.app_sync() )
            
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        
        asyncio.run( print_log_lora(f"LoRaWAN HTTP API: Driver Terminated") )


    async def terminate_service(self):
        self.status = False
        #self.device_db = [] #Memory freeed at shared memory py
 

    async def app_sync(self):  #update app mem
        for dev in get_loraWAN_db():
            if dev['online']:
                for fld in dev['data']:
                    if fld['online']:
                        for bnd in fld['binds']:
                            try:
                                await set_mem_value(bnd['app'], bnd['memalloc'], bnd['datatype'], fld['value'] )
                            except Exception as ex: 
                                error = f"Error, LoRaWAN Binding Error! {ex}\n devEUI: {dev['devEUI']} field: {fld['name']} \n "
                                await print_log_lora(error)

    def mile_to_json(self, rec):
        reslt = {
            "devEUI"        : str(rec['devEUI']),
            "applicationID" : str(rec['applicationID']),
            "deviceName"    : str(rec['deviceName']),
            "online"        : True,
            "data"          : [],
        }

        for key, value in rec.items():
            #print(key + ' ' + str(value))
            #if key != 'devEUI' and key != 'applicationID' and key != 'deviceName' and key != 'online':
            reslt['data'].append({ "name": key, "value": value, "online": True, "binds": [] }) # app, memalloc

        return reslt

    def mile_database_update(self, data): #update from socket (aka gateway)
        device_db = get_loraWAN_db()
        dev = find_device(device_db, data['devEUI'])
        
        if dev == None: #brand new device
           device_db.append( self.mile_to_json(data) )
        else: #update values
            dev['online']        = True
            dev['deviceName']    = data['deviceName']
            dev['applicationID'] = data['applicationID']
            if dev != None:
                for key, value in data.items():
                    fld = find_field(dev, key)
                    #print('Updated ' + key + ' = ' + str(fld['value']) + ' / ' + str(value))
                    if fld != None:
                        fld['value']  = value
                        fld['online'] = True
                    else:
                        dev['data'].append({ "name": key, "value": value, "online": True, "binds": [] }) 
        
        set_loraWAN_db(device_db)


def add_app_loraWAN_sync(app, datapoints):
    bind_count = 0 # app: name, fields: [{name: ;'', memalloc: 1}]

    device_db = get_loraWAN_db()

    for rec in datapoints:
        if rec['protocol']['enable']:
            bind_count += 1

            dev = find_device(device_db, rec['protocol']['devEUI'])
            if dev == None: #brand new device
                dev = {
                        "devEUI"        : str(rec['protocol']['devEUI']),
                        "applicationID" : '-1',
                        "deviceName"    : '?',
                        "online"        : False,
                        "data"          : [],
                    }
                device_db.append( dev ) #Add new Device

            fld = find_field(dev, rec['protocol']['field'])
            if fld == None:               
                fld = { "name": rec['protocol']['field'], "value": '?', "online": False, "binds": [] }
                dev['data'].append(fld)

            fld["binds"].append({'app': app, 'datatype': rec['datatype'], 'memalloc': rec['memalloc']})
        
    set_loraWAN_db(device_db)

    return bind_count
    

def free_app_loraWAN_sync(app):
    bind_count = 0
    device_db = get_loraWAN_db()
        
    for rec in device_db:
        for dt in rec['data']:
            for bnd in dt['binds']:
                if bnd['app'] == app:
                    bind_count += 1
                    dt['binds'].pop(dt['binds'].index(bnd))

    set_loraWAN_db(device_db)

    return bind_count


def find_device(device_db, devEUI):
    return next((item for item in device_db if item['devEUI'].lower() == devEUI.lower()), None)


def find_field( device, field ):
    #if key != 'devEUI' and key != 'applicationID' and key != 'deviceName' and key != 'online':
    return next((item for item in device['data'] if item['name'] == field), None)



#Get DB from Memory
def set_loraWAN_db(jsn):
    SERVER_MEM =  get_server_mem()
    SERVER_MEM[3] = ujson.dumps( jsn ) #ujson.dumps( jsn )


def get_loraWAN_db():
    return ujson.loads( get_server_mem()[3] )



