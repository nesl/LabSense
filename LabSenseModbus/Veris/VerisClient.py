import sys                              # For importing from parent directory
import os                               # For importing from parent directory

# Import from common directory
sys.path.insert(0, os.path.abspath(".."))
from common.modbus import TCPModbusClient

class VerisClient(TCPModbusClient):

    def __init__(self, name, IP, PORT):
        super(VerisClient, self).__init__(IP, PORT)
        self.devicename = "Veris"
        self.name = name

        # Veris configuration:
        # Modbus address = 1, Function Code = Read (3),
        # Starting register = 2083 (Power), 
        #                     2267 (Power Factor)
        #                     2251 (Current)
        # Number of registers to read = 42
        self.modbus_addr = 1
        self.modbus_func = 3
        self.reg_addresses = [2083, 2267, 2251]
        self.reg_qty = 42

        self.Valid_channels = ["Power", "PowerFactor", "Current"]
        self.sensor_names = self.Valid_channels

    """ Functions that must be implemented by child
    classes of TCPModbusClient """
    def getDeviceData(self, channels_to_record):
        device_data = {}
        channel_data = {}
        for channel in channels_to_record:
            address = self.getModbusAddressForChannel(channel)
            data = self.modbusReadReg(self.modbus_addr, self.modbus_func, address, self.reg_qty)
            parsed_data = self.parseData(data, address, channels_to_record)
            channel_data.update(parsed_data)

        return channel_data

    def parseData(self, data, modbus_address, channels_to_record):
        """ Maps the data received to the channels """
        if modbus_address == 2083:
            channel = "Power"
        elif modbus_address == 2267:
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
            address = 2267
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


