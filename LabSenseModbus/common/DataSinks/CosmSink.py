import sys, os                              # For importing from project directory
import json                                 # For writing cosm JSON message
#from datetime import datetime               # For formatting timestamp into Cosm's format
import time

from Cosm.CosmUploader import CosmUploader
import DataSink

class CosmSink(DataSink.DataSink):

    def __init__(self, config, queue, interval):
        super(CosmSink, self).__init__(config, queue, interval) 
        cosmConfig = config["Cosm"]
        self.cosmUploader = CosmUploader(cosmConfig["API_KEY"], cosmConfig["user_name"])
        self.feedids = {}

        # CosmSink's default behavior is to batch because it is rate-limited.
        self.batch = True

    def run(self):
        """ Overrides DataSink run function because Cosm can use batching """
        print "Starting DataSink"
        while True:

            if not self.queue.empty():
                if self.batch:
                    data = self.__queue_get_all()
                else:
                    data = self.queue.get()
                start_time = time.time()
                self.update(data)
                end_time = time.time()
                print "update elapsed time: %r, with %d items in queue. " % (end_time - start_time, self.queue.qsize())
            #else:
                #print "Queue was empty"

            time.sleep(self.interval)

    """ Helper functions """
    def __queue_get_all(self):
        """ Gets all items in a queue """
        items = []
        while not self.queue.empty():
            items.append(self.queue.get())
        return items

    """ Functions child classes must implement """

    def registerDevice(self, name):
        """ Registers a device to the service """
        feedid = self.cosmUploader.checkFeedPresent(name)

        # If the feed was not found, create it.
        if feedid == -1:
            feed_message = self.createFeed(name)
            feedid = self.cosmUploader.createFeed(feed_message)
        self.feedids[name] = feedid
        self.devices.append(name)

    def update(self, data):
        """ Updates Cosm with the data given """

        if self.batch:

            # All items in data are the same format. 
            # Thus, use the first item for all the metadata (device_name,
            # feed_id, etc)
            item = data[0]
            device_name = item["devicename"]
            device = item["device"]

            if device_name not in self.devices:
                self.registerDevice(device_name)

            feed_id = self.feedids[device_name]

            datastreams = []
            for item_index, item in enumerate(data):
                timestamp = item["timestamp"]
                cosmTimestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(timestamp))

                channel_counter = 0
                for sensor_name, channels in item["channels"].iteritems():
                    for channel in channels["measurements"]:

                        datapoint = {"at": cosmTimestamp, "value": channel[1]}
                        if item_index == 0:
                            # If this is first time going through items, create
                            # the datastreams
                            unit = {"label": channels["units"]}
                            datastream = {"id": channel[0], 
                                          "current_value": channel[1], 
                                          "unit": unit, 
                                          "datapoints": [datapoint]
                                         }
                            datastreams.append(datastream)

                        else:
                            # If not first time, add to the datastreams created
                            # already
                            datastreams[channel_counter]["current_value"] = channel[1]
                            datastreams[channel_counter]["datapoints"].append(datapoint)
                        channel_counter += 1

            message = {"version": "1.0.0",
                       "datastreams": datastreams
                      }

            self.cosmUploader.update(json.dumps(message), feed_id)


        else:

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
