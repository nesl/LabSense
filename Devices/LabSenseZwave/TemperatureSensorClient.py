from ZwaveClient import ZwaveClient

class TemperatureSensorClient(ZwaveClient):

    def __init__(self, name, IP, PORT, channels):
        super(TemperatureSensorClient, self).__init__(IP, PORT, channels)
        self.name = name

    def _formatChannelData(self, current_time, device,
                           device_name):
        """ Returns channel data in internal json format """
        channel_data = {}
        # Temperature Sensor has temperature reading in Fahrenheit
        if "Temperature" not in self.channels:
            return None

        # Only return data if Temperature channel is specified
        channel_data["Temperature"] = {
            "units": "Fahrenheit",
            "measurements": [
                ("Temperature", str(device["temperature"]))]}

        device_data = {"devicename": device_name,
                       "timestamp": current_time,
                       "channels": channel_data
                       }
        return device_data
