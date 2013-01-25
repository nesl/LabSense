import argparse                         # For parsing command line arguments
from EatonClient import EatonClient
from SensorAct.EatonSensorActFormatter import EatonSensorActFormatter 
import time                             # For getting the timestamp
import sys                              # For importing from parent directory
import os                               # For importing from parent directory

# Import from common directory
sys.path.insert(0, os.path.abspath(".."))
from common.SensorAct.SensorActUploader import SensorActRemoteForwarder
from common.Cosm.CosmUploader import CosmUploader
from common.Cosm.CosmFormatter import CosmFormatter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("IP", help="IP address for Eaton")
    parser.add_argument("PORT", help="Port for Eaton")
    parser.add_argument("Name", help="Unique Eaton Name")
    parser.add_argument("Location", help="Location of Eaton")
    parser.add_argument("-SensorActIP", help="SensorAct IP address")
    parser.add_argument("-SensorActPort", help="SensorAct Port")
    parser.add_argument("-SensorActApiKey", help="SensorAct Api Key")
    parser.add_argument("-SensorActSInterval", help="Sampling Interval for\
            SensorAct sensor", default=60)
    parser.add_argument("-CosmApiKey", help="SensorAct Api Key")
    args = parser.parse_args()

    #channels = ["VoltageAB", "CurrentA", "CurrentB", "CurrentC", "PowerFactorA",
            #"PowerFactorTotal", "PowerA", "PowerB", "PowerTotal"]
    channels = ["VoltageAN", "VoltageBN", "VoltageCN", 
                       "VoltageAB", "VoltageBC", "VoltageCA",
                       "CurrentA", "CurrentB", "CurrentC",
                       "PowerTotal", "VARsTotal", "VAsTotal",
                       "PowerFactorTotal", "Frequency", "NeutralCurrent",
                       "PowerA", "PowerB", "PowerC",
                       "VARsA", "VARsB", "VARsC",
                       "VAsA", "VAsB", "VAsC",
                       "PowerFactorA", "PowerFactorB", "PowerFactorC"]
    client = EatonClient(args.IP, args.PORT, channels)
    client.connect()
    data = client.getData()

    print "DATA: " + str(data)

    uploaders = []

    timestamp = time.time()
    if args.SensorActIP and args.SensorActPort and args.SensorActApiKey and\
        args.SensorActSInterval:
        sensorActformatter = EatonSensorActFormatter(args.Name, 
                                            args.SensorActApiKey,  
                                            args.SensorActSInterval,
                                            args.Location,
                                            channels)
                                            
        saForwarder = SensorActRemoteForwarder(args.SensorActIP, args.SensorActPort)
        uploaders.append((sensorActformatter, saForwarder))

    #if args.CosmApiKey:
        #cosmformatter = CosmFormatter(args.Name,
                                      #args.CosmApiKey,
                                      #args.Location,
                                      #channels)
        ##cosmForwarder = SensorActRemoteForwarder(args.CosmIP, args.CosmPort)
        #cosmForwarder = CosmUploader(args.CosmApiKey)
        #uploaders.append((cosmformatter, cosmForwarder))

    for uploader in uploaders:
        # Format the data
        formatted_data = uploader[0].format(data, timestamp)
        #formatted_data = uploader[0].format(data)
        print "Formatted Data: " + str(formatted_data)

        # Forward the formatted data
        for message in formatted_data:
            #uploader[1].send("VoltageAB", message)
            uploader[1].send(message)
            uploader[1].receive()

        #uploader[1].send("VoltageAB", formatted_data)
        #uploader[1].receive()
