import argparse                         # For parsing command line arguments
import sys                              # For importing from parent directory
import os                               # For importing from parent directory
import httplib                          # For making http requests to Vera 
import json                             # For reading JSON returned from Vera

class ZwaveClient(object):

    def __init__(self, IP, PORT, channels):
        self.IP = IP
        self.PORT = PORT
        self.channels = channels
        #self.__connect()

    def getData(self):

        device_data = {}
        channel_data = self.__getDeviceData()
        json_chan_data = json.loads(channel_data)
        return json_chan_data["devices"]

    """ Functions Called within ZwaveClient """
    def __connect(self):
        self.connection = httplib.HTTPConnection(self.IP, self.PORT)

    def __getDeviceData(self):
        self.__connect()
        url = "/data_request?id=sdata&output_format=json"
        self.connection.request("GET", url)
        response = self.__receive()
        return response.read()
        self.connection.close()

    def __receive(self):
        try:
            response = self.connection.getresponse()
        except httplib.BadStatusLine:
            print "Bad status!"
            pass
        return response



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("IP", help="IP of ZwaveClient")
    parser.add_argument("PORT", help="PORT of ZwaveClient")
    args = parser.parse_args()

    channels = ["Power", "Energy"]
    client = ZwaveClient(args.IP, args.PORT, channels)

    data = client.getData(["Power", "Energy"])
    print data
