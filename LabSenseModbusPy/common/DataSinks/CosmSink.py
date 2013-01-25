from Cosm.CosmUploader import CosmUploader
from DataSink import DataSink
import LabSenseHandler.configReader as config
from SensorAct.EatonSensorActFormatter import EatonSensorActFormatter

class CosmSink(DataSink):

    def __init__(self):
        super(CosmSink, self).__init__()
        self.config = config.config["Cosm"]
        self.cosmUploader = CosmUploader()

    def update(self, data):
        messages = []

        device = data["device"]

        if device == "Eaton":
            formatter = EatonCosmFormatter()

        elif device == "Raritan":
            pass
