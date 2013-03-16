import json                                 # Used for reading json
import os                                   # To change to this directory

""" When reading in a JSON file into a dictionary, the elements are read in as unicode. This function converts it to the strings. """
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
    """ Reads the LabSense configuration file """
    with open(config_file) as config:
        config = json.load(config)
    config = convert(config)
    return config
