import argparse                         # For parsing command line arguments
import sys                              # For importing from parent directory
import os                               # For importing from parent directory
from sets import Set                    # For unordered subset checking

# Import from common directory
sys.path.insert(0, os.path.abspath(".."))
from common.modbus import TCPModbusClient

""" EatonClient inherits from the TCPModbusClient, which can read data from any
modbus device. EatonClient adds a level on top to specify what fields should
be read from the Eaton meter, instead of needing to look up the registers that
correspond to fields. """
class EatonClient(TCPModbusClient):

    # Initializes EatonClient and verifies fields are valid
    def __init__(self, IP, PORT, fields):

        super(EatonClient, self).__init__(IP, PORT)

        Valid_fields = Set(["VoltageAN", "VoltageBN", "VoltageCN", 
                           "VoltageAB", "VoltageBC", "VoltageCA",
                           "CurrentA", "CurrentB", "CurrentC",
                           "PowerTotal", "VARSTotal", "VAsTotal",
                           "PowerFactorTotal", "Frequency", "NeutralCurrent",
                           "PowerA", "PowerB", "PowerC",
                           "VARSA", "VARSB", "VARSC",
                           "VAsA", "VAsB", "VAsC",
                           "PowerFactorA", "PowerFactorB", "PowerFactorC"])

        if not fields.issubset(Valid_fields):
            raise KeyError("Eaton fields given were not recognized")

    # Gets data from the EatonMeter
    def getData(self):  
        # Eaton configuration: 
        # Modbus address = 1, Function Code = Read (3), Starting register = 999,
        # Number of registers = 54
        data = self.modbusReadReg(1, 3, 999, 54)
        return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("IP", help="IP address for Eaton")
    parser.add_argument("PORT", help="Port for Eaton")
    args = parser.parse_args()

    fields_to_read = Set(["CurrentA", "CurrentB", "CurrentC"])
    client = EatonClient(args.IP, args.PORT, fields_to_read)
    client.connect()
    client.getData()
