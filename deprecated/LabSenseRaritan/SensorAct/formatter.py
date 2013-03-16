import json

class RaritanFormatter():

    def __init__(self, secretkey, data, timestamp):
        self.data = data
        self.timestamp = timestamp
        self.numOutlets = 8
        self.secretkey = secretkey

    def format(self):
        all_bodies = []

        for outlet in range(self.numOutlets):
            body = {}
            body["secretkey"] = self.secretkey

            body["data"] = self.generateData(outlet)

            all_bodies.append(json.dumps(body))


        return all_bodies

    def generateData(self, outlet):
        data = {}
        data["dname"] = "NESL_Raritan"

        # Outlet is 1-based, not 0-based
        oneBasedOutlet = outlet + 1

        data["sname"] = "Outlet" + str(oneBasedOutlet)
        data["sid"] = str(oneBasedOutlet)
        data["sinterval"] = 60
        data["timestamp"] = self.timestamp
        data["loc"] = "BH1762/UCLA"
        data["channels"] = self.generateChannels(outlet)

        return data

    def generateChannels(self, outlet):
        all_channels = []

        channelNames = ["Current", "Voltage", "Active Power", "Apparent Power", "Power Factor"]
        channelUnits = ["mA", "mv", "Watts", "Volt-amps", "Percent"]

        for index, chanName in enumerate(channelNames):
            channel = {}
            channel["cname"] = chanName
            channel["unit"] = channelUnits[index]

            # 8 readings are sent per channel
            channelIndex = outlet + (index * 8)
            channel["readings"] = [self.data[channelIndex]]

            all_channels.append(channel)

        return all_channels
