import json                                 # Used for reading json
import os                                   # To change to this directory

""" When reading in a JSON file into a dictionary, the elemnts are read in as unicode. This function converts it to the strings. """
def convert(unicode_dict):
    if isinstance(unicode_dict, dict):
        return {convert(key): convert(value) for key, value in unicode_dict.iteritems()}
    elif isinstance(unicode_dict, list):
        return [convert(element) for element in unicode_dict]
    elif isinstance(unicode_dict, unicode):
        return unicode_dict.encode('utf-8')
    else:
        return unicode_dict 


def readConfiguration(config_file):
    config_file_path = os.path.abspath(os.path.dirname(__file__)) + "/" + config_file
    with open(config_file_path) as config:
        config = json.load(config)
    
    config = convert(config)

    recognized_keys = ["SensorAct", "Cosm", "Eaton",
                       "Veris", "Raritan", "Stdout", "Zwave", "SmartSwitch", 
                       "LabSenseServer"]

    for key in config:
        if key not in recognized_keys:
            raise KeyError(key + " is not a recognized key.")

    return config

config = readConfiguration("config.json")
