import httplib, urllib
import json

class CosmFormatter(object):

    def __init__(self, secretkey, location, channels):
        self.secretkey = secretkey
        self.location = location
        self.channels = channels

    def listFeeds(self):
        pass

    def createFeed(self, feed_title):
        feed_data = { "title": feed_title, "version": "1.0.0"}
        return json.dumps(feed_data)

    def updateDatastream(self, data_stream, current_value):
        update_data = {"id": data_stream, "current_value": current_value}
        return json.dumps(update_data)

    def close(self):
        self.connection.close()

    def receive(self):
        response = self.connection.getresponse()
        print response.status, response.reason
        data = response.read()
        print data

        return data

    def send(self, data):
        print "Sending remotely: \n" + data
        self.connection.request("POST", "/data/upload/wavesegment", data, self.headers)
