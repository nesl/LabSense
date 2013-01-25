import argparse                         # For parsing command line arguments
import sys                              # For importing from parent directory
import os                               # For importing from parent directory
import time                             # For recording timestamp when getting data

# Import from common directory
sys.path.insert(0, os.path.abspath(".."))
from common.modbus import TCPModbusClient

""" EatonClient inherits from the TCPModbusClient, which can read data from any
modbus device. EatonClient adds a level on top to specify what channels should
be read from the Eaton meter, instead of needing to look up the registers that
correspond to channels. """
class EatonClient(TCPModbusClient):

    # Initializes EatonClient and verifies channels are valid
    def __init__(self, name, IP, PORT):
        self.name = name
        super(EatonClient, self).__init__(IP, PORT)
        self.Valid_channels = ["VoltageAN", "VoltageBN", "VoltageCN", 
                           "VoltageAB", "VoltageBC", "VoltageCA",
                           "CurrentA", "CurrentB", "CurrentC",
                           "PowerTotal", "VARsTotal", "VAsTotal",
                           "PowerFactorTotal", "Frequency", "NeutralCurrent",
                           "PowerA", "PowerB", "PowerC",
                           "VARsA", "VARsB", "VARsC",
                           "VAsA", "VAsB", "VAsC",
                           "PowerFactorA", "PowerFactorB", "PowerFactorC"]


    def checkValidChannel(self, channels):
        print "channels : " + str(channels)
        if not all([channel in self.Valid_channels for channel in channels]):
            raise KeyError("Eaton channels given were not recognized")
        return True

    # Gets data from the EatonMeter
    def getData(self, channels_to_record):  
        self.checkValidChannel(channels_to_record)

        # Eaton configuration: 
        # Modbus address = 1, Function Code = Read (3), Starting register = 999,
        # Number of registers = 54
        current_time = time.time()
        data = self.modbusReadReg(1, 3, 999, 54)

        device_data = {}
        if data:
            channel_data = {}
            channel_data_pairs = dict(zip(self.Valid_channels, data))

            sensor_names = ["Voltage", "Current", "PowerFactor", "VARs", "VAs",
                    "Power", "Frequency"]
            for sensor_name in sensor_names:
                channel_data[sensor_name] = []

            used_channels = []

            for chan in self.Valid_channels:
                for sensor_name in sensor_names:
                    if sensor_name in chan and chan not in used_channels and chan in channels_to_record:
                        key_val_pair = (chan, channel_data_pairs[chan])
                        #key_val_pair = {}
                        #key_val_pair = {chan: channel_data_pairs[chan]}
                        channel_data[sensor_name].append(key_val_pair)
                        used_channels.append(chan)

            print "Channel data: " + str(channel_data)

            device_data = {"devicename": self.name,
                           "device": "Eaton",
                           "timestamp": current_time,
                           "channels": channel_data
                          }
        
        return device_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("IP", help="IP address for Eaton")
    parser.add_argument("PORT", help="Port for Eaton")
    args = parser.parse_args()

    channels = ["CurrentA", "CurrentB", "CurrentC"]
    client = EatonClient(args.IP, args.PORT, channels)
    client.connect()
    client.getData()
