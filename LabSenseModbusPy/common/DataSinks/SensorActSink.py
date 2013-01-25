import time                                 # For sleeping between sensoract transfers
import sys, os                              # For importing from project directory
from DataSink import DataSink
from SensorAct.EatonSensorActFormatter import EatonSensorActFormatter
from SensorAct.SensorActUploader import SensorActForwarder

# Import from project directory
sys.path.insert(0, os.path.abspath("../.."))
import LabSenseHandler.configReader as config

class SensorActSink(DataSink):

    def __init__(self):
        super(SensorActSink, self).__init__()
        self.config = config.config["SensorAct"]
        self.sensorActForwarder = SensorActForwarder(self.config["IP"], self.config["PORT"])


    def update(self, data):
        messages = []

        device = data["device"]
        if device == "Eaton":
            formatter = EatonSensorActFormatter()
            formatted_data = formatter.format(self.config["API_KEY"], data)

        elif device == "Raritan":
            raise NotImplementedError("Haven't\
                    implemented Raritan SensorAct Sink")

        for message in formatted_data:
            self.sensorActForwarder.send(message)

