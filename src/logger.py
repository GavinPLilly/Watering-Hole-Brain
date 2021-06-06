# Module imports
from datetime import datetime

# My imports
import get_prop

FILE_STUB = get_prop.get_prop("FILE_STUB", "s")
ERROR_FILE = get_prop.get_prop("ERROR_LOG_FILE", "s")
EVENT_FILE = get_prop.get_prop("EVENT_LOG_FILE", "s")


# log(msg: String, filename: String): void
def log(msg, filename):
    file_handle = None
    try:
        file_handle = open(filename, 'a')
        file_handle.write(str(datetime.now()) + " " + msg + "\n")
    except:
        __backup_log(msg)
    if(file_handle != None):
        file_handle.close()

def log_error(msg):
    log(msg, ERROR_FILE)

def log_event(msg):
    log(msg, EVENT_FILE)

def __backup_log(msg):
    filename = FILE_STUB + str(datetime.now())
    print(filename)
    file_handle = open(filename, 'a')
    file_handle.write(str(datetime.now()) + " " + msg + "\n")
    file_handle.close()
