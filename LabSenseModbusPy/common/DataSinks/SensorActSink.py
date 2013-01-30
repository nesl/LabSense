import time                                 # For sleeping between sensoract transfers
import sys, os                              # For importing from project directory
from DataSink import DataSink
from SensorAct.SensorActUploader import SensorActUploader

import json 

class SensorActSink(DataSink):

    """ Initializes SensorActSink with config, which is a
    dictionary constructed from config.json and contains
    info about SensorAct and the rest of the
    sensors/sinks. """
    def __init__(self, config):
        super(SensorActSink, self).__init__()
        self.config = config

        sensorActConfig = config["SensorAct"]
        self.sensorActUploader = SensorActUploader(sensorActConfig["IP"], sensorActConfig["PORT"])

    def registerDevice(self, device_name, name):
        if device_name not in self.devices:
            self.devices.append(device_name)

        ####### TODO: ADD REGISTER DEVICE
        ####### CODE

    def getSensorName(self, channel_name):
        sensor_name = ""
        if "Voltage" in channel_name:
            sensor_name = "Voltage"
        elif "Current" in channel_name:
            sensor_name = "Current"
        elif "PowerFactor" in channel_name:
            sensor_name = "PowerFactor"
        elif "VARs" in channel_name:
            sensor_name = "VARs"
        elif "VAs" in channel_name:
            sensor_name = "VAs"
        elif "Power" in channel_name:
            sensor_name = "Power"
        else:
            raise NotImplementedError("No such sensor name for channel " + channel_name)

        return sensor_name

    def update(self, data):
        messages = []

        device = data["device"]

        device_config = self.config[device]

        print "Device config: " + str(device_config["channels"])
        print "Data channels: " + str(data["channels"])

        formatted_data_messages = []
        for sensor_name, channels in data["channels"].iteritems():
            message = {}
            formatted_data = {}
            formatted_data = {"dname": device_config["name"], 
                              "sname": sensor_name,
                              "sinterval": device_config["sinterval"],
                              "timestamp": data["timestamp"],
                              "loc": device_config["location"],
                             }
            channel_list = []
            for channel in channels["measurements"]:
                channel_data = {"cname": channel[0],
                                "unit": channels["units"],
                                "readings": [channel[1]]
                               }
                channel_list.append(channel_data)

            formatted_data["channels"] = channel_list
            message = {"secretkey": self.config["SensorAct"]["API_KEY"], "data": formatted_data }

            formatted_data_messages.append(json.dumps(message))

        for message in formatted_data_messages:
            self.sensorActUploader.send(message)

