from datetime import datetime

FILE_STUB = "/home/gavin/well-man/WellFlex/Watering-Hole-Brain/files/"
ERROR_FILE = FILE_STUB + "error_log"
EVENT_FILE = FILE_STUB + "event_log"


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
