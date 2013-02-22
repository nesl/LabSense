from ZwaveClient import ZwaveClient

class LightSensorClient(ZwaveClient):

    def __init__(self, name, IP, PORT, channels):
        super(LightSensorClient, self).__init__(IP, PORT, channels)
        self.name = name

    def _formatChannelData(self, current_time, device,
                           device_name):
        """ returns channel data in internal json
        format """
        channel_data = {}
        # Light Sensor has light reading
        channel_data["Light"] = {"units": "Percent",
                                 "measurements": [
                                 ("Light", str(device["light"]))]}

        device_data = {"devicename": device_name,
                       "device": device_name,
                       "timestamp": current_time,
                       "channels": channel_data
                       }
        return device_data
