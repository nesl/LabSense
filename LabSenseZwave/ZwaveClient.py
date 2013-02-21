import argparse                         # For parsing command line arguments
import time                             # For recording timestamp when getting data
from VeraClient import VeraClient       # For zwave

class ZwaveClient(object):

    def __init__(self, IP, PORT, channels):
        self.zwaveClient = VeraClient(IP, PORT, channels)

    def getData(self):
        current_time = time.time()
        data = self.zwaveClient.getData()

        device_data = []
        for device in data:
            device_name = device["name"]
            channel_data = {}
            if device_name == "NESL_SmartSwitch":
                # SmartSwitch has Power and Energy
                channel_data["Power"] = {"units": "Watts",
                        "measurements": [ ("Power", str(device["watts"]))]}
                channel_data["Energy"] = {"units": "kwh",
                                         "measurements": [ ("Energy", str(device["kwh"]))]}

            elif device_name == "NESL_LightSensor":
                # Light Sensor has light reading
                channel_data["Light"] = {"units": "Percent",
                                         "measurements": [
                                         ("Light", str(device["light"]))]}
            elif device_name == "NESL_TemperatureSensor":
                # Temperature Sensor has temperature reading in Fahrenheit
                channel_data["Temperature"] = {
                    "units": "Fahrenheit",
                    "measurements": [
                        ("Temperature", str(device["temperature"]))]}

            device_data = {"devicename": device_name,
                           "device": device_name,
                           "timestamp": current_time,
                           "channels": channel_data
                           }

            device_datas.append(device_data)

        return device_data

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
    client = ZwaveClient("NESL_SmartSwitch", args.IP, args.PORT, channels)

    data = client.getData()
    print data
