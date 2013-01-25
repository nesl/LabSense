import httplib

class CosmUploader(object):

    def __init__(self, api_key):
        self.cosm_url = "api.cosm.com"
        self.headers = {"X-ApiKey": api_key}
        self.connect()

    def connect(self):
        self.connection = httplib.HTTPConnection(self.cosm_url)

    def createFeed(self, params):
        self.connection.request("POST", "/v2/feeds", params, self.headers)

    def updateDatastream(self, data_stream, body):
        url = "/v2/feeds/datastreams/" + data_stream        
        print "URL: " + url
        self.connection.request("PUT", url, body, self.headers)

    def send(self, data_stream, params):
        self.updateDatastream(data_stream, params)
        pass

    def receive(self):
        response = self.connection.getresponse()

        print response.status, response.reason
        data = response.read()
        print data
        return data

