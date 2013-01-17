import argparse         # For reading command line arguments
import socket           # For TCP Socket: create_connection and htons()
import struct           # For reading/writing binary data
import crc16            # For calculating crc-16 for modbus msgs
import logging          # For logging events
import sys              # For printing out response bytes

class TCPModbusClient(object):

    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.server_addr = (str(IP), int(PORT))

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

        print "Packed data: " + repr(packed_data)

        self.sock.sendall(packed_data)
    
        # Response size is:
        #   Modbus Address 1 byte
        #   Function Code  1 byte
        #   Number of data bytes to follow 1 byte
        #   Register contents reg_qty * 2 b/c they are 16 bit values
        #   CRC 2 bytes
        response_size = 5 + 2*reg_qty
        response = self.getResponse(response_size)
        return response

    def getResponse(self, size):
        response = self.sock.recv(size)

        struct_format = "!" + "B" * size
        data = struct.unpack(struct_format, response)

        print "Response length: " + str(len(response))
        sys.stdout.write("Response: ")
        for num in data:
            sys.stdout.write(hex(num) + " " )

        return data


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
    

