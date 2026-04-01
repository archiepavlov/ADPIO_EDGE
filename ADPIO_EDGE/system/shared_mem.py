from multiprocessing.shared_memory import ShareableList

server_mem_name = 'server_mem'

def init_server_mem(mile_alloc = 100, terminal = False):
    try:
        SERVER_MEM = ShareableList(name=server_mem_name) 
        SERVER_MEM.shm.close()
        SERVER_MEM.shm.unlink()
    except:
        if __debug__:
            print("Server Memory Not Exists")

    SERVER_MEM = ShareableList( [
        0,              # Server Status 0 - Not Init, 1 - Run Signal, 2 - Shutdown Signal
        0,              # Workers Count
        terminal,       #Ouput into Terminal
        " " * 1024 * mile_alloc, # loraWAN Serialized Size may be too small (in 1024 x kb )
    ], name=server_mem_name)

    SERVER_MEM[3] = "[]"

    if __debug__:
        print("Shared Mem Initialized")
        


def clear_server_mem():
    SERVER_MEM = get_server_mem()

    SERVER_MEM.shm.close()
    SERVER_MEM.shm.unlink()


def get_server_mem():
    try:
        return ShareableList(name=server_mem_name) 
    except:
        print("Server Memory Does not exist")
        return [
            2,   # Server Status 0 - Not Init, 1 - Run Signal, 2 - Shutdown Signal
            -1,  # Workers Count
            False,
            "[]"
        ]
