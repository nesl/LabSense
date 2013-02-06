import sys, os                              # For importing from project directory
import json                                 # For writing cosm JSON message
#from datetime import datetime               # For formatting timestamp into Cosm's format
import time


from Cosm.CosmUploader import CosmUploader
from DataSink import DataSink

class CosmSink(DataSink):

    def __init__(self, config, queue, interval):
        super(CosmSink, self).__init__(interval, queue)
        self.config = config

        cosmConfig = config["Cosm"]
        self.cosmUploader = CosmUploader(cosmConfig["API_KEY"], cosmConfig["user_name"])
        self.feedids = {}

    """ Functions child classes must implement """

    def __registerDevice(self, name):
        """ Registers a device to the service """
        feedid = self.cosmUploader.checkFeedPresent(name)

        # If the feed was not found,
        # create it.
        if feedid == -1:
            feed_message = self.createFeed(name)
            feedid = self.cosmUploader.createFeed(feed_message)
        self.feedids[name] = feedid
        self.devices.append(name)

    def update(self, data):
        """ Updates Cosm with the data given """

        device_name = data["devicename"]
        device = data["device"]

        if device_name not in self.devices:
            self.__registerDevice(device_name)

        feed_id = self.feedids[device_name]
        timestamp = data["timestamp"]
        cosmTimestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(timestamp))

        datastreams = []
        for sensor_name, channels in data["channels"].iteritems():
            for channel in channels["measurements"]:
                
                datapoint = {"at": cosmTimestamp, "value": channel[1]}
                unit = {"label": channels["units"]}
                datastream = {"id": channel[0], 
                              "current_value": channel[1], 
                              "unit": unit, 
                              "datapoints": [datapoint]
                             }
                datastreams.append(datastream)

        message = {"version": "1.0.0",
                   "datastreams": datastreams
                  }

        self.cosmUploader.update(json.dumps(message), feed_id)

    """ Helper functions """
    def createFeed(self, feed_title):
        feed_data = { "title": feed_title, "version": "1.0.0"}
        return json.dumps(feed_data)
