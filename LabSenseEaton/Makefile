OBJS1 = TCPModbusServer.o DieWithError.o HandleModbusTCPClient.o crc16.o utility.o
#OBJS6 = TCPModbusClient.o DieWithError.o crc16.o utility.o #TRG = TCPModbusServer TCPModbusClient CC = gcc
#DEBUG = -g
CC = gcc
DEPS = zhelpers.h E30ModbusMsg.h
LIBS = -lzmq
CFLAGS = -Wall $(DEBUG) -I.
#LFLAGS = -Wall $(DEBUG) -lzmq

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

TCPModbusClient: $(OBJS1)
	$(CC) -o TCPModbusClient $(OBJS1) -I. $(LIBS)

#TCPModbusServer : $(OBJS1)
	#$(CC) $(LFLAGS) $(OBJS1) -o TCPModbusServer

#TCPModbusClient : $(OBJS6)
	#$(CC) $(LFLAGS) $(OBJS6) -o TCPModbusClient 

#TCPModbusServer.o : TCPModbusServer.c
	#$(CC) -c $(CFLAGS) TCPModbusServer.c

#TCPModbusClient.o : TCPModbusClient.c
	#$(CC) -c $(CFLAGS) TCPModbusClient.c -lzmq

#DieWithError.o : DieWithError.c
	#$(CC) -c $(CFLAGS) DieWithError.c

#HandleModbusTCPClient.o : HandleModbusTCPClient.c E30ModbusMsg.h
	#$(CC) -c $(CFLAGS) HandleModbusTCPClient.c

#crc16.o : crc16.c
	#$(CC) -c $(CFLAGS) crc16.c

#utility.o : utility.c zhelpers.h
	#$(CC) -c $(CFLAGS) utility.c -lzmq -I /usr/include/
##crc16.o : crc16.c
	##$(CC) -c $(CFLAGS) crc16.c

##utility.o : utility.c zhelpers.h
	##$(CC) -c $(CFLAGS) utility.c -lzmq -I /usr/include/

clean:
	rm *.o $(TRG)


