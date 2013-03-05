import httplib, urllib

class SensorActUploader(object):
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.headers = { "Content-type": "application/json",
                      "Accept": "text/plain" }

    def connect(self):

        self.connection = httplib.HTTPConnection(self.IP + ":" + str(self.PORT))

    def close(self):
        self.connection.close()

    def receive(self):
        try:
            response = self.connection.getresponse()
            print "SensorAct ", response.status, response.reason
        except httplib.BadStatusLine:
            print "Bad status!"
            response = None
        return response

    def send(self, data):
        sent = False
        while sent == False:
            try:
                self.connect()
                self.connection.request("POST", "/data/upload/wavesegment", data, self.headers)
                response = self.receive()
                self.connection.close()

                if response.status == 200:
                    # If response was 200 break out of loop
                    sent = True
            except IOError:
                print ("No internet connection, will send the data when the internet"
                      " becomes available")
                time.sleep(5)


if __name__ == "__main__":
    forwarder = SensorActLocalForwarder("asdf", "asdf")
    forwarder.receive()
