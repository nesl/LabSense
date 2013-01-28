import time                                 # For sleeping between sensoract transfers
import sys, os                              # For importing from project directory
from DataSink import DataSink
from SensorAct.EatonSensorActFormatter import EatonSensorActFormatter
from SensorAct.SensorActUploader import SensorActUploader

import json 

# Import from project directory
sys.path.insert(0, os.path.abspath("../.."))
import LabSenseHandler.configReader as config

class SensorActSink(DataSink):

    def __init__(self):
        super(SensorActSink, self).__init__()
        self.config = config.config["SensorAct"]
        self.sensorActUploader = SensorActUploader(self.config["IP"], self.config["PORT"])

    def registerDevice(self, device_name, name):
        if device_name not in self.devices:
            self.devices.append(device_name)

        ####### TODO: ADD REGISTER DEVICE
        ####### CODE


    def getSensorNameUnit(self, sensor_name):
        units = ""
        if sensor_name == "Voltage":
            units = "Volts"
        elif sensor_name == "Current":
            units = "Amps"
        elif sensor_name == "Power":
            units = "Watts"
        elif sensor_name == "VARs":
            units = "VARs"
        elif sensor_name == "VAs":
            units = "VAs"
        elif sensor_name == "PowerFactor":
            units = "None"
        else:
            raise NotImplementedError("No such sensor name")

        return units


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
        #if device == "Eaton":
            #formatter = EatonSensorActFormatter()
            #formatted_data = formatter.format(self.config["API_KEY"], data)

        #elif device == "Raritan":
            #raise NotImplementedError("Haven't\
                    #implemented Raritan SensorAct Sink")

        device_config = config.config[device]

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
            for channel in channels:
                channel_data = {"cname": channel[0],
                                "unit": self.getSensorNameUnit(sensor_name),
                                "readings": [channel[1]]
                               }
                channel_list.append(channel_data)

            formatted_data["channels"] = channel_list
            message = {"secretkey": self.config["API_KEY"],
                       "data": formatted_data }

            formatted_data_messages.append(json.dumps(message))

        for message in formatted_data_messages:
            self.sensorActUploader.send(message)

