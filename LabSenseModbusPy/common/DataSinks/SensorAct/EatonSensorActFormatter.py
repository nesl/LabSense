import sys, os                              # For importing from project directory
import json
import copy

# Import from project directory
sys.path.insert(0, os.path.abspath("../.."))
import LabSenseHandler.configReader as config

class EatonSensorActFormatter():

    #def __init__(self, name, apikey, sinterval, location, channels):
    def __init__(self):
        self.config = config.config["Eaton"]
        self.initializeUnitsDictionary()
        self.parseChannels()

    def initializeUnitsDictionary(self):
        self.units = {}
        self.units["VoltageAN"] = "Volts"
        self.units["VoltageBN"] = "Volts"
        self.units["VoltageCN"] = "Volts"
        self.units["VoltageAB"] = "Volts"
        self.units["VoltageBC"] = "Volts"
        self.units["VoltageCA"] = "Volts"
        self.units["CurrentA"] = "Amps"
        self.units["CurrentB"] = "Amps"
        self.units["CurrentC"] = "Amps"
        self.units["PowerTotal"] = "Watts"
        self.units["VARsTotal"] = "VARs"
        self.units["VAsTotal"] = "VAs"
        self.units["PowerFactorTotal"] = "None"
        self.units["Frequency"] = "Hertz"
        self.units["NeutralCurrent"] = "Amps"
        self.units["PowerA"] = "Watts"
        self.units["PowerB"] = "Watts"
        self.units["PowerC"] = "Watts"
        self.units["VARsA"] = "VARs"
        self.units["VARsB"] = "VARs"
        self.units["VARsC"] = "VARs"
        self.units["VAsA"] = "VAs"
        self.units["VAsB"] = "VAs"
        self.units["VAsC"] = "VAs"
        self.units["PowerFactorA"] = "None"
        self.units["PowerFactorB"] = "None"
        self.units["PowerFactorC"] = "None"

    """ Parses the channels into a dictionary organized in the following way:
    
        channels[sensor_name] = [channel1, channel2..]

        Example:
        channels_dict["Voltage"] = ["VoltageAN", "VoltageBN"...]
    """
    def parseChannels(self):
        channels = self.config["channels"]
        if not all([field in self.units.keys() for field in channels]):
            raise NotImplementedError("Unrecognized fields given for Eaton Meter.")

        self.channels_dict = {}

        # Note that ordering is important. PowerFactor must come before Power
        # and VARs before VAs because to check Power is a part of PowerFactor,
        # and substring checks are used to determine sensor_names.
        self.sensor_names = ["Voltage", "Current", "PowerFactor", "VARs", "VAs",
                "Power", "Frequency"]

        for sensor_name in self.sensor_names:
            self.channels_dict[sensor_name] = []

        # Keeps track of used channels so that Power Factor readings are not
        # sent under both the Power Factor channel and the Power channel.
        # (VARs and VA's too)
        used_channels = []

        for chan in self.config["channels"]:
            for sensor_name in self.sensor_names:
                if sensor_name in chan and chan not in used_channels:
                    self.channels_dict[sensor_name].append(chan)
                    used_channels.append(chan)

    def format(self, apikey, data_values):
        messages = []

        timestamp = data_values["timestamp"]

        for sensor_name in self.sensor_names:

            if self.channels_dict[sensor_name]:
                message = {}
                message["secretkey"] = apikey
                message["data"] = self.generateData(sensor_name, timestamp, data_values["channels"]) 
                messages.append(json.dumps(message))

        return messages

    def generateData(self, sensor_name, timestamp, data_values):
        data = {"dname": self.config["name"],
                "sname": sensor_name,
                "sinterval": self.config["sinterval"],
                "timestamp": timestamp,
                "loc": self.config["location"]
               }
        data["channels"] = self.generateChannels(sensor_name, data_values)

        return data

    def generateChannels(self, sensor_name, data_values):
        channel_data = []

        channels = []
        channels = self.channels_dict[sensor_name]

        for channel in channels: 
            data = {}
            data["cname"] = channel
            data["unit"] = self.units[channel]
            data["readings"] = [data_values[channel]]
            channel_data.append(data)

        return channel_data

