import asyncio
import sys

from pony.orm import *

#Shared Memory
from multiprocessing.shared_memory    import ShareableList


#<LIBIMPORT/>

from terminal import terminal_web
from app_lib import  __app_db_runtime
from dataconversion import str_to_dp


APP_NAME   = "nonameapp"
app_db     = None


async def startup(shared_mem):
    global app_db
    
    app_db = __app_db_runtime(APP_NAME)
    app_db.init_db()
    
    with db_session:
        dp = app_db.datapoints.select()
        
        for d_rec in dp:
            shared_mem[d_rec.memalloc] = str_to_dp(d_rec.value, d_rec.datatype, fallback = True)
        
        sys.stdout.write(f"{APP_NAME} Loading Datapoint Values (Count {len(dp)})...\n")


async def save_current_values(shared_mem):
    global app_db
    
    dp_ids = []
    with db_session:    #Save All Datapoints
        dp = app_db.datapoints.select()
        
        for d_rec in dp:
            dp_ids.append(d_rec.id)
       
    with db_session:    
        for d_id in dp_ids:        
            up_rec = app_db.datapoints[d_id]
            up_rec.value = str(shared_mem[up_rec.memalloc])
            

async def terminate(shared_mem):
    await save_current_values(shared_mem)
    app_db.close_db()


async def trends_sync(shared_mem, trend_list, sleep):
    global app_db

    for tr in trend_list:
        tr["left"] -= sleep
        
        if tr["left"] <= 0 and tr["old_value"] != shared_mem[tr["memalloc"]]:
            tr["old_value"] = shared_mem[tr["memalloc"]]
            tr["left"] = tr["refresh"]     
            
            with db_session:                           
                app_db.trends (         
                    name     = tr['name'],
                    value    = str(shared_mem[tr["memalloc"]]),
                    datatype = tr['datatype'],
                )
    
    return trend_list


async def exec():
    terminal = terminal_web(f'apps_{APP_NAME}', True)

    SLEEP      = 1
    sys.stdout.write(f'APP {APP_NAME} Initializing...\n')

#Shared Mems
    shared_mem = ShareableList( [
            True, 0, #Default Field: Status/Loop Count
            #<DATAPOINTS_LENGTH/>
            
            #<DATAPOINTS_DEF/>
        ], name=f'{APP_NAME}_sharedmem' # track=False, for py 3.13+
    )

#Binds
    bind_mem = ShareableList( [
            #<BINDS_LENGTH/> #Buffer Length
            
            #<BINDS_DEF/>
        ], name=f'{APP_NAME}_bindmem' #track=False, for py 3.13+
    )

#Trends
    trends = [
        #<TRENDS_INIT>
    ]

    sys.stdout.write(f'APP {APP_NAME} Started, Shared Mem Name: {APP_NAME}_sharedmem, Loop Delay: {SLEEP}\n')
  
    await startup(shared_mem)    
    #await write_defaults(shared_mem) #Writed Defaults
    
    while shared_mem[0]:
        try:
            await asyncio.sleep(SLEEP)

    #Gets
            #<GETTERS_CODE/>

    #Code
            #<BLOCK_CODE/>

    #Sets
            #<SETTERS_CODE/>
            
            if __debug__:
                shared_mem[1] += 1
                sys.stdout.write(f'LOOP EXECUTED. Status = {shared_mem[0]} , Loop = {shared_mem[1]}\n')
                if shared_mem[1] == 254:
                    shared_mem[1] = 0
                       
        except Exception as err:
            sys.stderr.write(f'APP {APP_NAME} Runtime Error : {err} \n')
        except:
            sys.stderr.write(f'APP {APP_NAME} Unnamed Error\n')
            shared_mem[0] = False

    #Trends loop
        trends = await trends_sync(shared_mem, trends, SLEEP)
               
    await terminate(shared_mem)
            
    #Clear Shared Memory
    shared_mem.shm.close()
    shared_mem.shm.unlink()
    
    bind_mem.shm.close()
    bind_mem.shm.unlink()

    sys.stdout.write(f'APP {APP_NAME} Terminated.\n')
    terminal.terminate()


if __name__ == "__main__":
    if __debug__: sys.stdout.write("DEBUG For APPS is on. Run with -O to turn off debug\n")

    asyncio.run( exec() )

