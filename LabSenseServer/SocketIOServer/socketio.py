from os import path as op
import time

import zmq
from zmq.eventloop import ioloop, zmqstream
ioloop.install()

import tornado.web
import tornadio
import tornadio.router
import tornadio.server

ROOT = op.normpath(op.dirname(__file__))

class LabSenseConnection(tornadio.SocketConnection):
    # Class level variable
    participants = set()
    channel = ""

    @classmethod
    def dispatch_message(cls, messages):
        for participant in cls.participants:

            for message in messages:
                print "CHANNEL: " + participant.channel
                print "Message: " + message
                json_msg = {}
                if participant.channel in message:
                    msg_list = message.split(" ")
                    json_msg["name"] = msg_list[0]
                    json_msg['data'] = msg_list[1:]
                    json_msg['timestamp'] = int(time.time())*1000
                    participant.send(json_msg)

    def on_open(self, *args, **kwargs):
        pass

    def on_message(self, message):
        self.channel = message["channel"]
        print self.channel
        self.participants.add(self)

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
    stream.on_recv(ChatConnection.dispatch_message)

    tornadio.server.SocketServer(application)
