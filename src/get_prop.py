# Module imports

# My imports

CONFIG_FILE = "/home/gavin/well-man/WellFlex/Watering-Hole-Brain/files/.config"

# get_prop(key: String, mode: String): String | number | boolean | []
def get_prop(key, mode):
    raw_line = __get_raw_line(key)
    if(raw_line == ''):
        import logger
        logger.log_error("Couldn't find key \"" + key + "\" in config file")
        return ''
    return __process_line(__get_raw_line(key), mode)

def __get_raw_line(key):
    
    try:
        file_handle = open(CONFIG_FILE)
    except:
        return None

    raw_line = ""
    while(True):
        cur_line = file_handle.readline()
        if(__check_for_match(cur_line, key)):
            raw_line = cur_line
            break
        if(cur_line == ''):
            break

    return raw_line

# __check_for_match(line: String, key: String): boolean
def __check_for_match(line, key):
    return line.find(key) == 0

# __process_line(raw_line: String, mode: String): String | number | boolean | []
def __process_line(raw_line, mode):
    key = __extract_raw_key(raw_line)
    value = __extract_raw_value(raw_line)
    add_stub = len(key) - key.rfind('FILE') == 4
    if(value.find('[') == 0 and value.find(']') == len(value) - 1):
        return __process_array(value, mode)
    return __process_value(value, mode, add_stub)

# __process_value(value: String, mode: String, add_stub: boolean): String | number | boolean
def __process_value(value, mode, add_stub):
    if(add_stub):
        value = get_prop("FILE_STUB", "s") + value
    if(mode == 'n'):
        return float(value)
    if(mode == 'b'):
        if(value == "True"):
            return True
        return False
    return str(value)

def __process_array(raw_array, mode):
    raw_list = raw_array.strip("[]").split(',')
    prepped_list = []
    for x in raw_list:
        prepped_list.append(x.strip())
    final_list = []
    for x in prepped_list:
        final_list.append(__process_value(x, mode, False))
    return final_list

# __extract_raw_value(raw_line: String): String
def __extract_raw_value(raw_line):
    if(raw_line.find(':') == -1):
        return ""
    split_list = raw_line.split(':')
    i = 2
    value_string = split_list[1]
    while(i < len(split_list)):
        value_string += (":" + split_list[i])
        i += 1

    return value_string.strip().rstrip('\n')

# __extract_raw_key(raw_line: String): String
def __extract_raw_key(raw_line):
    if(raw_line.find(':') == -1):
        return ""
    return raw_line.split(':')[0]
