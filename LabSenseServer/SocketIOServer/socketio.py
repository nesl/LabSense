from os import path as op
import time

import zmq
from zmq.eventloop import ioloop, zmqstream
ioloop.install()

import tornado.web
import tornadio
import tornadio.router
import tornadio.server

from SensorCacher import SensorCacher

ROOT = op.normpath(op.dirname(__file__))

cache = SensorCacher()

class LabSenseConnection(tornadio.SocketConnection):
    # Class level variable
    participants = set()
    channel = ""
    ready = False

    @classmethod
    def dispatch_message(cls, messages):
        for participant in cls.participants:

            for message in messages:
                print "CHANNEL: " + participant.channel
                print "Message: " + message
                json_msg = {}
                msg_list = message.split(" ")
                name = msg_list[0]
                data = msg_list[1:]
                timestamp = int(time.time())*1000

                if participant.channel in message and participant.ready == True:

                    if participant.channel == "Raritan" or participant.channel == "Veris":
                            json_msg["multiple"] = 1
                    else:
                        json_msg["multiple"] = 0
                    json_msg["bulk"] = 0
                    json_msg["name"] = name
                    json_msg['data'] = data
                    json_msg['timestamp'] = timestamp
                    participant.send(json_msg)

                storing_channel = message.split("_")[0]
                cache.createTable(storing_channel)
                cache.insertRow(storing_channel,name, data,
                        timestamp)

    def on_open(self, *args, **kwargs):
        pass

    def on_message(self, message):

        if message["action"] == "init":
            self.channel = message["channel"]
            name = message["name"]

            print "INITIALIZING " + str(self.channel)
            print "Name: " + str(name)

            results = cache.getChannelData(self.channel,name )

            data_list = []
            timestamp_list = []
            name_list = []
            for name, data, timestamp_str, timestamp in results:
                json_msg = {}
                if self.channel == "Raritan" or self.channel == "Veris":
                    json_msg["multiple"] = 1
                else:
                    json_msg["multiple"] = 0

                json_msg["bulk"] = 0
                json_msg["name"] = name
                json_msg["data"] = data
                json_msg["timestamp"] = timestamp

                self.send(json_msg)

            self.participants.add(self)
        elif message["action"] == "done":
            self.ready = True

    def on_close(self):
        self.participants.remove(self);

#use the routes classmethod to build the correct resource
LabSenseRouter = tornadio.get_router(LabSenseConnection, {
    'enabled_protocols': [
        'websocket',
        'flashsocket',
        'xhr-multipart',
        'xhr-polling'
    ]
})

#configure the Tornado application
application = tornado.web.Application(
    [LabSenseRouter.route()],
    flash_policy_port = 843,
    flash_policy_file = op.join(ROOT, 'flashpolicy.xml'),
    socket_io_port = 8001
)

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5556")
    socket.connect("tcp://localhost:5557")
    socket.connect("tcp://localhost:5558")
    socket.setsockopt(zmq.SUBSCRIBE, '')
    stream = zmqstream.ZMQStream(socket, tornado.ioloop.IOLoop.instance())
    stream.on_recv(LabSenseConnection.dispatch_message)

    tornadio.server.SocketServer(application)
