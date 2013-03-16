from formatter import RaritanFormatter 
from uploader import SensorActRemoteForwarder
from uploader import SensorActLocalForwarder
import time

class SensorActUploader(object):

    def __init__(self, conn_type, IP, PORT, API_KEY):
        self.conn_type = conn_type 
        self.IP = IP
        self.PORT = PORT
        self.secretkey = API_KEY

    def send(self, data, timestamp):
        formatter = RaritanFormatter(self.secretkey, data, timestamp)
        formatted_data = formatter.format()

        if self.conn_type == "local":
            forwarder = SensorActLocalForwarder()

        elif self.conn_type == "remote":
            forwarder = SensorActRemoteForwarder(self.IP, self.PORT)

        else:
            raise NotImplementedError

        for fdata in formatted_data:
            forwarder.send(fdata)
            forwarder.receive()
