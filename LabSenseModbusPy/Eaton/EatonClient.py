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
        super(EatonClient, self).__init__(IP, PORT)
        self.devicename = "Eaton"
        self.name = name

        # Eaton configuration: 
        # Modbus address = 1, Function Code = Read (3), Starting register = 999,
        # Number of registers = 54
        self.modbus_addr = 1
        self.modbus_func = 3
        self.reg_addresses = [999]
        self.reg_qty = 54
        self.Valid_channels = ["VoltageAN", "VoltageBN", "VoltageCN", 
                           "VoltageAB", "VoltageBC", "VoltageCA",
                           "CurrentA", "CurrentB", "CurrentC",
                           "PowerTotal", "VARsTotal", "VAsTotal",
                           "PowerFactorTotal", "Frequency", "NeutralCurrent",
                           "PowerA", "PowerB", "PowerC",
                           "VARsA", "VARsB", "VARsC",
                           "VAsA", "VAsB", "VAsC",
                           "PowerFactorA", "PowerFactorB", "PowerFactorC"]
        self.sensor_names = ["Voltage", "Current", "PowerFactor", "VARs", "VAs",
                    "Power", "Frequency"]

    """ Functions that must be implemented by child
    classes of TCPModbusClient """
    def parseData(self, data, modbus_address, channels_to_record):
        channel_data = {}
        if data:
            channel_data_pairs = dict(zip(self.Valid_channels, data))

            used_channels = []

            for chan in self.Valid_channels:
                for sensor_name in self.sensor_names:
                    if sensor_name in chan and chan not in used_channels and chan in channels_to_record:
                        key_val_pair = (chan, channel_data_pairs[chan])

                        if sensor_name not in channel_data.keys():
                            channel_data[sensor_name] = []

                        channel_data[sensor_name].append(key_val_pair)
                        used_channels.append(chan)

        return channel_data



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("IP", help="IP address for Eaton")
    parser.add_argument("PORT", help="Port for Eaton")
    args = parser.parse_args()

    channels = ["CurrentA", "CurrentB", "CurrentC"]
    client = EatonClient(args.IP, args.PORT, channels)
    client.connect()
    client.getData()
