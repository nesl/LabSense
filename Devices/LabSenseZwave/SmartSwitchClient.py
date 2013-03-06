from ZwaveClient import ZwaveClient

class SmartSwitchClient(ZwaveClient):

    def __init__(self, name, IP, PORT, channels):
        super(SmartSwitchClient, self).__init__(IP, PORT, channels)
        self.name = name

    def _formatChannelData(self, current_time, device,
                           device_name):
        """ Returns channel data in internal json format """
        channel_data = {}

        print "CHANNELS : " + str(self.channels)

        # SmartSwitch has Power and Energy
        if "Power" in self.channels:
            print "INCLUDING POWER"
            channel_data["Power"] = {"units": "Watts",
                    "measurements": [ ("Power", str(device["watts"]))]}
        if "Energy" in self.channels:
            print "INCLUDING ENERGY"
            channel_data["Energy"] = {"units": "kwh",
                                     "measurements": [ ("Energy", str(device["kwh"]))]}

        if channel_data == {}:
            # If no channel data was written, don't send device data.
            return None

        device_data = {"devicename": device_name,
                       "timestamp": current_time,
                       "channels": channel_data
                       }
        return device_data
