import httplib, urllib

class SensorActForwarder(object):

    def connect(self):
        raise NotImplementedError

    def receive(self):
        raise NotImplementedError

    def send(self):
        raise NotImplementedError

class SensorActRemoteForwarder(SensorActForwarder):

    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT

        print "IP: " + str(IP)
        print "PORT: " + str(PORT)
        self.headers = { "Content-type": "application/json",
                      "Accept": "text/plain" }
        super(SensorActRemoteForwarder, self).__init__()
        self.connect()

    def connect(self):

        self.connection = httplib.HTTPConnection(self.IP + ":" + str(self.PORT))

        print "Successfully connected to " + self.IP + ": " + str(self.PORT)

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

class SensorActLocalForwarder(SensorActForwarder):

    def __init__(self):
        super(SensorActLocalForwarder, self).__init__()

    def receive(self):
        print "Receiving"

    def send(self,data ):
        print "Sending locally: \n" + data


if __name__ == "__main__":
    forwarder = SensorActLocalForwarder("asdf", "asdf")
    forwarder.receive()
