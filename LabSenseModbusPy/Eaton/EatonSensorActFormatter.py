import json

class EatonSensorActFormatter():

    def __init__(self, name, secretkey, sinterval, location, channels):
        self.name = name
        self.secretkey = secretkey
        self.sinterval = sinterval
        self.location = location
        self.channels = channels
        self.initializeUnitsDictionary()
        self.num_phases = 3

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


    def format(self, data_values, timestamp):

        messages = []

        # Raritan has three phases. Each phases will have a message.
        phases = ["A", "B", "C"]
        for iterator, phase in enumerate(phases):
            message = {}
            message["secretkey"] = self.secretkey

            message["data"] = self.generateData(iterator, phase, timestamp, data_values) 

            messages.append(json.dumps(message))

        return messages

    def generateData(self, sid, phase, timestamp, data_values):

        data = {}
        data["dname"] = self.name
        data["sname"] = "Phase" + phase
        # Keep sensor number 1-based (thus add 1)
        data["sid"] = sid+1
        data["sinterval"] = self.sinterval
        data["timestamp"] = timestamp
        data["loc"] = self.location
        data["channels"] = self.generateChannels(sid, phase, data_values)

        return data

    def generateChannels(self, sid, phase, data_values):
        channel_data = []

        for iterator, channel in enumerate(self.channels): 
            data = {}
            data["cname"] = channel
            data["unit"] = self.units[channel]
            data["readings"] = data_values[sid + iterator*self.num_phases]
            channel_data.append(data)

        return channel_data

