import httplib                              # For making http connection to Cosm
import re                                   # Regex for extractinextracting feed id from cosm response
import json                                 # For parsing json return from cosm

class CosmUploader(object):

    def __init__(self, api_key, user_name):
        self.cosm_url = "api.cosm.com"
        self.user_name = user_name
        self.headers = {"X-ApiKey": api_key}
        self.connect()

    def connect(self):
        self.connection = httplib.HTTPConnection(self.cosm_url)

    def getFeeds(self):

        url = "/v2/feeds?user=" + self.user_name + "&content=summary"
        self.connection.request("GET", url, headers=self.headers)
        response = self.receive()

        print response.status, response.reason

        feeds = json.loads(response.read())
        feeds = feeds["results"]

        print feeds
        return feeds

    def checkFeedPresent(self, feed):
        cosmfeeds = self.getFeeds()

        for cosmfeed in cosmfeeds:
            if feed == cosmfeed["title"]:
                return cosmfeed["id"]
        return -1


    def createFeed(self, params):
        self.connection.request("POST", "/v2/feeds", params, self.headers)
        response = self.receive()

        location = response.getheader("location")
        feedid = self.extractFeedId(location)

        return feedid

    def update(self, body, feedid):
        url = "http://api.cosm.com/v2/feeds/" + str(feedid)
        print "URL: " + url
        self.connection.request("PUT", url, body, self.headers)
        response = self.receive()
        response.read()

    def receive(self):
        response = self.connection.getresponse()
        print response.status, response.reason

        return response


    """ Helper functions """

    """ Extracts the feed id from the location returned by
    Cosm """
    def extractFeedId(self, location):
        print location
        feedid = re.search(r"\d+$", location)
        return str(int(feedid.group()))
