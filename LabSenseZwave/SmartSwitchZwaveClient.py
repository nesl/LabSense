import argparse                         # For parsing command line arguments
import time                             # For recording timestamp when getting data
from ZwaveClient import ZwaveClient                                     # For zwave

class SmartSwitchZwaveClient(object):

    def __init__(self, name, IP, PORT, channels):
        self.devicename = "SmartSwitch"
        self.name = name
        self.channels = channels
        self.Valid_channels = ["Power", "Energy"]
        self.__checkValidChannel(channels)
        self.zwaveClient = ZwaveClient(IP, PORT, channels)

    def getData(self):
        current_time = time.time()
        data = self.zwaveClient.getData()

        for device in data:
            if device["name"] == self.devicename:

                channel_data = {}
                for channel in self.channels:
                    if channel == "Power":
                        channel_data["Power"] = {"units": "Watts",
                                "measurements": [ ("Power", str(device["watts"]))]}
                    elif channel == "Energy":
                        channel_data["Energy"] = {"units": "kwh",
                                                 "measurements": [ ("Energy", str(device["kwh"]))]}
                        
                device_data = {"devicename": self.name, 
                               "device": self.devicename,
                               "timestamp": current_time,
                               "channels": channel_data
                              }
                return device_data

        return {}

    def __checkValidChannel(self, channels):
        if not all([channel in self.Valid_channels for channel in channels]):
            raise KeyError("Channels given were not recognized")
        return True

            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("IP", help="IP of ZwaveClient")
    parser.add_argument("PORT", help="PORT of ZwaveClient")
    args = parser.parse_args()

    channels = ["Power", "Energy"]
    client = SmartSwitchZwaveClient("NESL_SmartSwitch", args.IP, args.PORT, channels)

    data = client.getData()
    print data
