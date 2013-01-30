import httplib, urllib

class SensorActUploader(object):
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT

        print "IP: " + str(IP)
        print "PORT: " + str(PORT)
        self.headers = { "Content-type": "application/json",
                      "Accept": "text/plain" }
        self.connect()

    def connect(self):

        self.connection = httplib.HTTPConnection(self.IP + ":" + str(self.PORT))
        print "Successfully connected to " + self.IP + ": " + str(self.PORT)

    def close(self):
        self.connection.close()

    def receive(self):
        response = self.connection.getresponse()
        print "SensorAct", response.status, response.reason
        data = response.read()
        print data

        return data

    def send(self, data):
        self.connection.request("POST", "/data/upload/wavesegment", data, self.headers)
        self.receive()


if __name__ == "__main__":
    forwarder = SensorActLocalForwarder("asdf", "asdf")
    forwarder.receive()
