import argparse                         # For parsing command line arguments
import sys                              # For importing from parent directory
import os                               # For importing from parent directory
import httplib                          # For making http requests to Vera 
import json                             # For reading JSON returned from Vera
import time                             # For timestamp

class ZwaveClient(object):

    def __init__(self, IP, PORT, channels):
        self.IP = IP
        self.PORT = PORT
        self.channels = channels

    def getData(self):
        """ Gets data from vera and formats it into internal json structure """
        current_time = time.time()
        data = self.__getJsonData()

        if data:
            device_data = []
            for device in data:
                device_name = device["name"]
                channel_data = {}
                if device_name == self.name:
                    device_data = self._formatChannelData(current_time, device, device_name)
                    return device_data
        else:
            return None

        # If the device was not found, raise an error
        raise KeyError(self.name + " was not found when querying the Vera.")

    """ Functions that must be implemented by children """
    def _formatChannelData(device):
        raise NotImplementedError("Classes that inherit from ZwaveClient must implement _formatChannelData")

    """ Functions Called within VeraClient """
    def __connect(self):
        self.connection = httplib.HTTPConnection(self.IP, self.PORT)

    def __getJsonData(self):
        """ Gets data in json format from Vera (Zwave Receiver) """
        device_data = {}
        channel_data = self.__getDeviceData()
        if channel_data:
            json_chan_data = json.loads(channel_data)
            return json_chan_data["devices"]
        else:
            return None

    def __getDeviceData(self):
        self.__connect()
        url = "/data_request?id=sdata&output_format=json"
        self.connection.request("GET", url)
        response = self.__receive()
        self.connection.close()
        if response:
            return response.read()
        else:
            return None

    def __receive(self):
        try:
            response = self.connection.getresponse()
        except httplib.BadStatusLine:
            print "Bad status!"
            return None
        return response



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("IP", help="IP of VeraClient")
    parser.add_argument("PORT", help="PORT of VeraClient")
    args = parser.parse_args()

    channels = ["Power", "Energy"]
    client = VeraClient(args.IP, args.PORT, channels)

    data = client.getData(["Power", "Energy"])
    print data
