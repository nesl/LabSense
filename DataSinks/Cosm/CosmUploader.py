import httplib                              # For making http connection to Cosm
import re                                   # Regex for extractinextracting feed id from cosm response
import json                                 # For parsing json return from cosm
import time                                 # For waiting between retries

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

        try:
            feeds = json.loads(response.read())
            feeds = feeds["results"]
        except ValueError:
            print "Error in JSON from Cosm."
            return None
        return feeds

    def checkFeedPresent(self, feed):
        cosmfeeds = self.getFeeds()

        if cosmfeeds:
            for cosmfeed in cosmfeeds:
                if feed == cosmfeed["title"]:
                    return cosmfeed["id"]
        return None

    def createFeed(self, params):
        self.connect()
        self.connection.request("POST", "/v2/feeds", params, self.headers)
        response = self.receive()

        location = response.getheader("location")
        feedid = self.extractFeedId(location)

        return feedid

    def update(self, body, feedid):
        print "Updating Cosm"

        sent = False
        while sent == False:
            try:
                self.connect()
                url = "http://api.cosm.com/v2/feeds/" + str(feedid)
                self.connection.request("PUT", url, body, self.headers)
                response = self.receive()

                if response:
                    print "Cosm: ", response.status, response.reason
                    print response.read()
                    self.connection.close()

                    if response.status == 200:
                        # If response was 200 break out of loop
                        sent = True

                # Otherwise, loop again

            except IOError, detail:
                print ("No internet connection, will send the data when the internet"
                      " becomes available")
                time.sleep(5)

    def receive(self):
        try:
            response = self.connection.getresponse()
            print "Cosm", response.status, response.reason
        #except httplib.BadStatusLine:
        except Exception:
            print "Exception when getting response from Cosm!"
            response = None
        return response


    """ Helper functions """

    """ Extracts the feed id from the location returned by
    Cosm """
    def extractFeedId(self, location):
        feedid = re.search(r"\d+$", location)
        return str(int(feedid.group()))
