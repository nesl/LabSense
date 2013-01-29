import sys, os                              # For importing from project directory
import json                                 # For writing cosm JSON message

from Cosm.CosmUploader import CosmUploader
from DataSink import DataSink
import LabSenseHandler.configReader as config
from SensorAct.EatonSensorActFormatter import EatonSensorActFormatter
from Cosm.CosmFormatter import CosmFormatter

class CosmSink(DataSink):

    def __init__(self, config):
        super(CosmSink, self).__init__()
        self.config = config

        cosmConfig = config["Cosm"]
        self.cosmUploader = CosmUploader(cosmConfig["API_KEY"], cosmConfig["user_name"])
        self.formatters = {}
        self.feedids = {}

    """ Registers a device to the service """
    def registerDevice(self, device_name, name):
        device_config = self.config[device_name]
        
        formatter = CosmFormatter(self.config["Cosm"]["API_KEY"],
                                  device_config["location"], 
                                  device_config["channels"])
        self.formatters[device_name] = formatter
        feedid = self.cosmUploader.checkFeedPresent(name)

        # If the feed was not found,
        # create it.
        if feedid == -1:
            feed_message = formatter.createFeed(name)
            feedid = self.cosmUploader.createFeed(feed_message)
        self.feedids[name] = feedid
        
        if device_name not in self.devices:
            self.devices.append(device_name)

    def update(self, data):
        device_name = data["devicename"]
        device = data["device"]

        feed_id = self.feedids[device_name]

        datastreams = []
        for sensor_name, channels in data["channels"].iteritems():
            for channel in channels["measurements"]:
                datastream = {"id": channel[0], "current_value": channel[1]}
                datastreams.append(datastream)

        message = {"version": "1.0.0",
                   "datastreams": datastreams
                  }

        self.cosmUploader.update(json.dumps(message), feed_id)
