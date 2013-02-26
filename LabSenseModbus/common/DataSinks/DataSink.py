import time                                 # For sleeping between data transfers
import threading                            # For threading datasinks
import sys                                  # For importing from common directory
import os                                   # For importing from common directory

class DataSink(threading.Thread):

    def __init__(self, config, queue, interval):
        threading.Thread.__init__(self)
        self.interval = float(interval)
        self.devices = []
        self.queue = queue
        self.config = config

        # Default behavior for Datasinks is not to batch.
        self.batch = False 

    def dataSinkFactory(sink_type, config, queue, interval):
        import StdoutSink
        import SensorActSink
        import CosmSink 

        """ DataSinkFactory that creates sinks based on their type """
        if sink_type == "SensorAct":
            return SensorActSink.SensorActSink(config, queue, interval)
        elif sink_type == "Cosm":
            return CosmSink.CosmSink(config, queue, interval)
        elif sink_type == "Stdout":
            return StdoutSink.StdoutSink(config, queue, interval)
        else:
            raise TypeError("Unrecognized Sink Type for DataSinkFactory: " + sink_type)
    # Make DataSinkFactory static so DataSinks does not
    # have to be instantiated to run.
    dataSinkFactory = staticmethod(dataSinkFactory)


    def run(self):
        print "Starting DataSink"
        while True:

            if not self.queue.empty():
                data = self.queue.get()
                if data:
                    start_time = time.time()
                    self.update(data)
                    end_time = time.time()
                    print "update elapsed time: %r, with %d items in queue. " % (end_time - start_time, self.queue.qsize())
            time.sleep(self.interval)

    """ Functions child classes must implement """

    def update(self, data):
        raise NotImplementedError("DataSink is an abstract class. sendData must\
                be implemented by classes that inherit from DataSink.")

    def __registerDevice(self, device_name, name):
        raise NotImplementedError("DataSink is an abstract class.\
                RegisterDevice must be implemented by classes that inherit\
                from DataSink.")
