OBJS1 = TCPModbusServer.o DieWithError.o HandleModbusTCPClient.o crc16.o utility.o
OBJS6 = TCPModbusClient.o DieWithError.o crc16.o utility.o
TRG = TCPModbusServer TCPModbusClient
CC = gcc
DEBUG = -g
CFLAGS = -Wall -c $(DEBUG)
LFLAGS = -Wall $(DEBUG)

all : $(TRG)

TCPModbusServer : $(OBJS1)
	$(CC) $(LFLAGS) $(OBJS1) -o TCPModbusServer

TCPModbusClient : $(OBJS6)
	$(CC) $(LFLAGS) $(OBJS6) -o TCPModbusClient

TCPModbusServer.o : TCPModbusServer.c
	$(CC) $(CFLAGS) TCPModbusServer.c

TCPModbusClient.o : TCPModbusClient.c
	$(CC) $(CFLAGS) TCPModbusClient.c

DieWithError.o : DieWithError.c
	$(CC) $(CFLAGS) DieWithError.c

HandleModbusTCPClient.o : HandleModbusTCPClient.c E30ModbusMsg.h
	$(CC) $(CFLAGS) HandleModbusTCPClient.c

crc16.o : crc16.c
	$(CC) $(CFLAGS) crc16.c

utility.o : utility.c
	$(CC) $(CFLAGS) utility.c

clean:
	rm *.o $(TRG)


