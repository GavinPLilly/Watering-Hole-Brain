# Module Imports
import time

# My imports
import sensor_wrapper
import logger
import database_wrapper
import get_prop

CHECK_FILE = get_prop.get_prop("TAKE_MEASUREMENTS_CHECK_FILE", "s")

FREQUENCY = get_prop.get_prop("MEASUREMENT_FREQUENCY", "n")

SENSOR = sensor_wrapper.GeneralSensor(get_prop.get_prop("MOCK", "b"))

# runnner(): void
def runner():
    while(check_continue()):
        # Take measurement and add it to database
        record_measurement()
        time.sleep(FREQUENCY)

# check_continue(): boolean
def check_continue():
    check_file_handle = None
    file_content = None
    try:
        check_file_handle = open(CHECK_FILE, "r")
        file_content = check_file_handle.read()
    except:
        logger.log_error("take_measurements check file not found")

    if(check_file_handle != None):  # try to close the check file
        check_file_handle.close()

    return check_continue_helper(file_content)  # return whether the result of the file check

# check_continue_helper(contents: String): boolean
def check_continue_helper(contents):
    if(contents == "run"):
        return True
    if(contents == "run "):
        return True
    if(contents == "run\n"):
        return True
    if(contents == "run \n"):
        return True
    return False

# record_measurement(): void
def record_measurement():
    # get Sensor measurement
    # add it to database
    level = SENSOR.get_percent()
    database_wrapper.add_water_record(level)

runner()
