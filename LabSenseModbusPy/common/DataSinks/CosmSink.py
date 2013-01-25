class CosmSink(DataSink):

    def __init__(self):
        super(CosmSink, self).__init__()
        self.config = config.config["Cosm"]
        self.cosmForwarder = CosmForwarder(self.config["IP"], self.config["PORT"])

    def update(self, data):
