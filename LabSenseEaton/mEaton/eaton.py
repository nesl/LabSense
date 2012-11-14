import socket
import CRC16
import sys

TCP_IP = "128.97.11.100"
#TCP_IP = "172.17.5.177"
TCP_PORT = 4660
data = " ".join(sys.argv[1:])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((TCP_IP, TCP_PORT))
except Exception, e:
    alert('Could not connect to ' + str(TCP_IP) + ":" + str(TCP_PORT))

print "Connected!"

try:
    #print "Sending data: " + data
    #s.send("01 03 75 40 00 08")
    #data = "\0d"
    #data = "AT\0d"
    #s.sendall(data)
    #s.sendall("01 03 75 35 00 01")
    data = "\x01\x03\xC7\x57\x00\x10"
    crc = CRC16.calcString(data, CRC16.INITIAL_MODBUS)
    data = data + str("%x" % crc)
    print "data: " + data
    s.sendall(data + "\x0d")

    print "About to receive data"
    line = s.recv(8)
    print "Received data"

finally:
    s.close()

if line:
    print line
