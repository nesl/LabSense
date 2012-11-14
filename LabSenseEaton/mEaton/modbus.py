#from pymodbus.client.sync import ModbusTcpClient
from pymodbus.client.sync import ModbusSerialClient
import pymodbus

try:
    #client = ModbusTcpClient("128.97.11.100", "4660")
    #client = ModbusSerialClient("172.17.5.177", "4660", baudrate=9600)
    client = ModbusSerialClient(method="rtu", port="4660", baudrate=9600)
#except pymodbus.exceptions.ConnectionException, e:
except Exception, e:
    print "Connection Problem: " + str(e)

result = client.read_input_registers(1030, 1)
print "Result: " + str(result)
client.close()
