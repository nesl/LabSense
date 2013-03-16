import argparse                         # For parsing command line arguments
import sys                              # For importing from parent directory
import os                               # For importing from parent directory
import time                             # For recording timestamp when getting data

# Import from common directory
import Devices.LabSenseModbus.common.modbus as modbus

""" EatonClient inherits from the TCPModbusClient, which can read data from any
modbus device. EatonClient adds a level on top to specify what channels should
be read from the Eaton meter, instead of needing to look up the registers that
correspond to channels. """
class EatonClient(modbus.TCPModbusClient):

    # Initializes EatonClient and verifies channels are valid
    def __init__(self, name, IP, PORT, channels):
        super(EatonClient, self).__init__(IP, PORT)
        self.name = name
        self.channels = channels

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
        self.checkValidChannel(channels)

    """ Functions that must be implemented by child
    classes of TCPModbusClient """
    def getDeviceData(self):
        device_data = {}
        channel_data = {}
        for address in self.reg_addresses:
            data = self.modbusReadReg(self.modbus_addr, self.modbus_func, address, self.reg_qty)
            parsed_data = self.parseData(data, address, )
            channel_data.update(parsed_data)

        return channel_data

    def parseData(self, data, modbus_address):
        channel_data = {}
        if data:
            channel_data_pairs = dict(zip(self.Valid_channels, data))

            used_channels = []

            for chan in self.Valid_channels:
                for sensor_name in self.sensor_names:
                    if sensor_name in chan and chan not in used_channels and chan in self.channels:
                        key_val_pair = (chan, channel_data_pairs[chan])

                        if sensor_name not in channel_data.keys():
                            channel_data[sensor_name] = {}
                            channel_data[sensor_name]["measurements"] = []
                            channel_data[sensor_name]["units"] = self.getUnitsForChannel(sensor_name)

                        channel_data[sensor_name]["measurements"].append(key_val_pair)
                        used_channels.append(chan)

        return channel_data

    """ Helper functions """
    def getUnitsForChannel(self, channel):
        units = ""
        if channel == "Voltage":
            units = "Volts"
        elif channel == "Current":
            units = "Amps"
        elif channel == "Power":
            units = "Watts"
        elif channel == "VARs":
            units = "VARs"
        elif channel == "VAs":
            units = "VAs"
        elif channel == "PowerFactor":
            units = "None"
        else:
            raise NotImplementedError("No such channel name")

        return units


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("IP", help="IP address for Eaton")
    parser.add_argument("PORT", help="Port for Eaton")
    args = parser.parse_args()

    channels = ["CurrentA", "CurrentB", "CurrentC"]
    client = EatonClient(args.IP, args.PORT, channels)
    client.connect()
    client.getData()
