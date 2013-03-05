from ZwaveClient import ZwaveClient

class SmartSwitchClient(ZwaveClient):

    def __init__(self, name, IP, PORT, channels):
        super(SmartSwitchClient, self).__init__(IP, PORT, channels)
        self.name = name

    def _formatChannelData(self, current_time, device,
                           device_name):
        """ Returns channel data in internal json format """
        channel_data = {}
        # SmartSwitch has Power and Energy
        channel_data["Power"] = {"units": "Watts",
                "measurements": [ ("Power", str(device["watts"]))]}
        channel_data["Energy"] = {"units": "kwh",
                                 "measurements": [ ("Energy", str(device["kwh"]))]}

        device_data = {"devicename": device_name,
                       "timestamp": current_time,
                       "channels": channel_data
                       }
        return device_data
