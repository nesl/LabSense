import httplib, urllib
import json

class CosmFormatter(object):

    def __init__(self, secretkey, location, channels):
        self.secretkey = secretkey
        self.location = location
        self.channels = channels


    def format(self, data_values):
        #return createFeed("NESL_Eaton", ["VoltageAN"])
        return self.updateDatastream("VoltageAB", "123.333")

    def listFeeds(self):
        pass

    def createFeed(self, feed_title):
        feed_data = { "title": feed_title, "version": "1.0.0"}

        #id_datastreams = []
        #for datastream in data_streams:
            #id_dict = {}
            #id_dict["id"] = datastream
            #id_datastreams.append(id_dict)

        #feed_data["datastreams"] = id_datastreams

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


if __name__ == "__main__":

    cosmUploader = CosmUploader()
