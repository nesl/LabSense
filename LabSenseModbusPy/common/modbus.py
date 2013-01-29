import argparse         # For reading command line arguments
import socket           # For TCP Socket: create_connection and htons()
import struct           # For reading/writing binary data
import crc16            # For calculating crc-16 for modbus msgs
import logging          # For logging events
import sys              # For printing out response bytes
import time             # For timestamping data retrieval

class TCPModbusClient(object):

    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.server_addr = (str(IP), int(PORT))
        self.connect()

    def connect(self):
        self.sock = socket.create_connection(self.server_addr)

    def send(self, msg):
        pass

    def modbusReadReg(self, addr, modbus_func, reg_addr, reg_qty):

        # Create request with network endianness
        struct_format = ("!BBHH")
        packed_data = struct.pack(struct_format, addr, modbus_func, reg_addr, reg_qty)

        packed_data_size = struct.calcsize(struct_format)

        # Calculate the CRC16 and append to the end
        crc = crc16.calcCRC(packed_data)
        crc = socket.htons(crc)
        struct_format = ("!BBHHH")
        packed_data = struct.pack(struct_format, addr, modbus_func, reg_addr, reg_qty, crc)

        #print "Packed data: " + repr(packed_data)

        self.sock.sendall(packed_data)
    
        response = self.getResponse(reg_qty)
        return response

    def getResponse(self, reg_qty):
        # Response size is:
        #   Modbus Address 1 byte
        #   Function Code  1 byte
        #   Number of data bytes to follow 1 byte
        #   Register contents reg_qty * 2 b/c they are 16 bit values
        #   CRC 2 bytes
        response_size = 5 + 2*reg_qty
        response = self.sock.recv(response_size)

        struct_format = "!BBB" + "f" * (reg_qty/2) + "H"

        try:
            data = struct.unpack(struct_format, response)
        except struct.error:
            print "Received bad data. Skipping..."
            return []

        #print "Response length: " + str(len(response))
        # Remove first 3 bytes and last two bytes (See
        # above)
        start = 3
        end = start + (reg_qty/2)
        data = data[start:end]

        sys.stdout.write("Response: ")
        for num in data:
            sys.stdout.write(str(num) + " " )

        print "\n"
        return data


    """ Channel-level calls for getting
    data from meters """

    # Checks if channels given are valid
    def checkValidChannel(self, channels):
        if not all([channel in self.Valid_channels for channel in channels]):
            raise KeyError("Channels given were not recognized")
        return True

    # Gets data from the meter
    def getData(self, channels_to_record):  
        self.checkValidChannel(channels_to_record)

        current_time = time.time()
        device_data = {}
        channel_data = {}
        for address in self.reg_addresses:
            data = self.modbusReadReg(self.modbus_addr, self.modbus_func, address, self.reg_qty)
            parsed_data = self.parseData(data, address, channels_to_record)
            channel_data.update(parsed_data)

        if channel_data:
            device_data = {"devicename": self.name,
                           "device": self.devicename,
                           "timestamp": current_time,
                           "channels": channel_data
                          }
        return device_data

    """ Functions that must be implemented by child classes. """

    def parseData(self, data, modbus_address):
        raise NotImplementedError("ParseData must be implemented by all child classes of TCPModbusClient.")

    def mapChannels(self, modbus_reg_addr, data):
        raise NotImplementedError("Map channels function must implemented in all TCPModbusClient children classes")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("IP", help="IP address for device")
    parser.add_argument("PORT", help="Port for device")
    parser.add_argument("Modbus_address", help="Modbus\
            address")
    parser.add_argument("Modbus_funct_code", help="Modbus function code")
    parser.add_argument("Modbus_start_reg", help="Modbus\
            starting register")
    parser.add_argument("Modbus_num_regs", help="Number of registers")
    args = parser.parse_args()

    client = TCPModbusClient(args.IP, args.PORT)
    client.connect()
    data = client.modbusReadReg(int(args.Modbus_address),
                         int(args.Modbus_funct_code),
                         int(args.Modbus_start_reg),
                         int(args.Modbus_num_regs))
    

