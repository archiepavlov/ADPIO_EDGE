# ADPIO EDGE - IOT, FLOW-BASED PROGRAMMING AND INTEGRATION PLATFORM
Modern IOT and fully WEB-based platform. 

## [WEBSITE: ADPIO EDGE](http://adpioedge.com)


Build around 3 main fundamentals: 
1. Datapoint agregation and integration
2. Flow based programming
3. GUI builder.
4. Simple Trends
5. LoRaWAN Integration

At this moment works on linux only. 

Dependencies for Python:
```
  python312 - PonyORM lagging behind, this is why py 3.12 is used
  uvicorn
  uvloop
  fastapi
  ujson
  pony
  psutil #cpu and mem info
```

Dependencies for Svelte (required only for dev):
```
  nodejs_24
  svelte with typescript
  carbon-icons-svelte
  js-cookie  
```

## Upcoming Milestones
1. BIP driver, BACnet Browser And BACnet Integration
2. More Graphical Widgets
3. Raspberry PI IO
4. Modbus Integration
5. MQTT Server
6. Windows Support (Meh, eventually)


## Quick Start
Instructions on getting started:
1. `./start_adpio.sh` or `./start_adpio.sh debug`
2. Open <http://localhost:8000>
3. Login with default credentials admin/admin
4. Navigate to Logic Palette and click Rebuild Database
   
## Pair Milesight LoRaWan Gateway (ex UG65) with LoRaWAN driver
[Reference Documentation](https://support.milesight-iot.com/support/solutions/articles/73000514208-how-to-connect-milesight-lorawan-gateway-to-http-s-server-)
1. Login to UG65 and Navigate to Network Server -> Applications
2. Create application if needed
3. Edit application -> add HTTP transmission
4. At the Uplink Data feild enter folowing: http://ip_of_adpio_edge:9002
