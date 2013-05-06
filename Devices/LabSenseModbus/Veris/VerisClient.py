import sys                              # For importing from parent directory
import os                               # For importing from parent directory
import argparse                         # For running the client from command line

# Import from common directory
import Devices.LabSenseModbus.common.modbus as modbus

class VerisClient(modbus.TCPModbusClient):

    def __init__(self, name, IP, PORT, channels):
        super(VerisClient, self).__init__(IP, PORT)
        self.name = name
        self.channels = channels

        # Veris configuration:
        # Modbus address = 1, Function Code = Read (3),
        # Starting register = 2083 (Power), 
        #                     2167 (Power Factor)
        #                     2251 (Current)
        # Number of registers to read = 42
        self.modbus_addr = 1
        self.modbus_func = 3
        self.reg_addresses = [2083, 2167, 2251]
        self.reg_qty = 42

        self.Valid_channels = ["Power", "PowerFactor", "Current"]
        self.sensor_names = self.Valid_channels
        self.checkValidChannel(channels)

    """ Functions that must be implemented by child
    classes of TCPModbusClient """
    def getDeviceData(self):
        device_data = {}
        channel_data = {}
        for channel in self.channels:
            address = self.getModbusAddressForChannel(channel)
            data = self.modbusReadReg(self.modbus_addr, self.modbus_func, address, self.reg_qty)
            parsed_data = self.parseData(data, address)
            channel_data.update(parsed_data)

        return channel_data

    def parseData(self, data, modbus_address):
        """ Maps the data received to the channels """
        if modbus_address == 2083:
            channel = "Power"
        elif modbus_address == 2167:
            channel = "PowerFactor"
        elif modbus_address == 2251:
            channel = "Current"

        channel_data = {}
        channel_list = []
        for iteration, value in enumerate(data):
            channel_name = channel + str(iteration)
            channel_value_pair = (channel_name, value)
            channel_list.append(channel_value_pair)

        channel_data[channel] = {}
        channel_data[channel]["measurements"] = channel_list
        channel_data[channel]["units"] = self.getUnitsForChannel(channel)
        return channel_data

    """ Helper functions """

    def getModbusAddressForChannel(self, channel):
        if channel == "Power":
            address = 2083
        elif channel == "PowerFactor":
            address = 2167
        elif channel == "Current":
            address = 2251
        return address

    def getUnitsForChannel(self, channel):
        units = ""
        if channel == "Current":
            units = "Amps"
        elif channel == "Power":
            units = "kW"
        elif channel == "PowerFactor":
            units = "None"
        else:
            raise NotImplementedError("No such channel name")

        return units

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("Name", help="Name of Veris meter")
    parser.add_argument("IP", help="IP of Veris meter")
    parser.add_argument("PORT", help="PORT of Veris meter")
    parser.add_argument("Channels", help="Channels to read")

    args = parser.parse_args()

    channels = [channel for channel in args.Channels.split(" ")]

    verisClient = VerisClient(args.Name, args.IP, args.PORT, channels)
    data = verisClient.getData()
    print data
