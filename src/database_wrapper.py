# Module imports
import mariadb
import sys
from datetime import datetime

# my imports
import logger

DB_PASSWORD_FILE = "/home/gavin/well-man/WellFlex/Watering-Hole-Brain/files/db_password"
DATABASE_NAME = "water_records"

# get_password(): String
def __get_password():
    pw_file_handle = None
    password = ""
    try:
        pw_file_handle = open(DB_PASSWORD_FILE, 'r')
        password = pw_file_handle.readline()
        password = password.rstrip('\n')
    except:
        logger.log_error("Problem reading db password file")

    if(pw_file_handle != None):
        pw_file_handle.close()

    return password

# add_water_record(level: int): void
def add_water_record(level):
    try:
        conn = mariadb.connect(
                user = "gavin",
                password = __get_password(),
                host = "localhost",
                port = 3306,
                database = DATABASE_NAME
                )
    except:
        logger.log_error("Problem connecting to MariaDB in add_water_record()")
        return

    try:
        # Get cursor
        cur = conn.cursor()

        level = int(round(level, 3) * 1000)
        cur.execute("INSERT INTO records (level, time) VALUES (?, NOW());", (level,))
        
        conn.commit()

    except:
        logger.log_error("Problem writing to database in add_water_record()")

    finally:
        conn.close()

# get_24h_records(): (number[], datetime[])
def get_24h_records():
    try:
        conn = mariadb.connect(
            user = "gavin",
            password = __get_password(),
            host = "localhost",
            port = 3306,
            database = DATABASE_NAME
            )
    except:
        logger.log_error("Problem connecting to MariaDB in get_daily_records()")
        return
                               
    try: 
        # Get cursor           
        cur = conn.cursor()
            
        cur.execute("SELECT level,time FROM records WHERE TIMESTAMPDIFF(DAY, time, NOW())=0;")
        level_array = []
        datetime_array = []
        for (level, time) in cur:
            level_array.append(level / 1000)
            datetime_array.append(time)
    except:
        logger.log_error("Problem getting daily records from database in get_daily_records()")
        return None
    
    finally:
        conn.close()

    return (level_array, datetime_array)
    
# delete_old_records(): void
def delete_old_records():
    conn = __get_cursor("delete_old_records()")
    if(conn == None):
        logger.log_error("error getting db cursor in delete_old_records(). Aborted")
        return 

    try: 
        # Get cursor           
        cur = conn.cursor()

        cur.execute("DELETE FROM records WHERE TIMESTAMPDIFF(DAY, time, NOW()) > 30;")

        conn.commit()

    except:
        logger.log_error("Problem deleting old records from database")

    finally:
        conn.close()

# get_newest_entry(): (number, datetime)
def get_newest_entry():
    conn = __get_cursor("get_newest_entry()")
    if(conn == None):
        logger.log_error("error getting db cursor in get_newest_entry()")
        return None

    try:
        cur = conn.cursor()

        cur.execute("SELECT level,time FROM records ORDER BY id DESC LIMIT 0,1")

        tup = next(cur)

        return (tup[0] / 1000, tup[1])
        
    except:
        logger.log_error("Problem getting newest entry from database")

    finally:
        conn.close()

# gen___get_cursor(): __get_cursor
def gen___get_cursor():
    # __get_cursor(calling_method: String): <Mariadb cursor object>
    pwd = __get_password()
    def __get_cursor(calling_method):
        conn = None
        try:
            conn = mariadb.connect(
                user = "gavin",
                password = pwd,
                host = "localhost",
                port = 3306,
                database = DATABASE_NAME
                )
        except:
            logger.log_error("Problem connecting to MariaDB in " + calling_method)

        return conn
    return __get_cursor

__get_cursor = gen___get_cursor()
