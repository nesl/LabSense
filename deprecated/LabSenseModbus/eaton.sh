#!/bin/bash

IP=128.97.11.100
MODBUS_PORT=4660
MODBUS_ADDR=1
MODBUS_REG=51031
MODBUS_NREGS=16

LOGPATH=$1
if [ -z "$LOGPATH" ]; then
  LOGPATH=log1
else
  mkdir $LOGPATH
fi

#while [ 1 ]; do 
  TIME=`date +%s`

  #DATA1=`./TCPModbusClient r $IP 4660 1 279 1 2>&1 | grep -A 1 float | grep "\."`
  #DATA1=`./TCPModbusClient r $IP 4660 1 1 1 2>&1`

  # Query port currently connected to
  #QUERY1=`echo "Querying port" && ./TCPModbusClient r $IP $MODBUS_PORT $MODBUS_ADDR 4499 1 2>&1`
  #sleep 1

  ## Reading Historical Log Header Block
  #DATA1=`echo "Reading Historical Log Header Block" && ./TCPModbusClient r $IP $MODBUS_PORT $MODBUS_ADDR $MODBUS_REG $MODBUS_NREGS 2>&1`
  #sleep 1

  ## Enable the Log 
  #LOG_ENABLE=`echo "Enabling the Log" && ./TCPModbusClient w $IP $MODBUS_PORT $MODBUS_ADDR 49999 640 2>&1`
  #sleep 1

  ## Reading Historical Log Block Again
  #DATA2=`echo "Reading Historical Log Block Again" && ./TCPModbusClient r $IP $MODBUS_PORT $MODBUS_ADDR $MODBUS_REG $MODBUS_NREGS 2>&1`
  
  #DATA3=`echo "Reading Meter Type" && ./TCPModbusClient r $IP $MODBUS_PORT 1 30014 1 2>&1` 
  DATA3=`echo "Reading Meter Type" && ./TCPModbusClient r eaton` 
  #if [ -n "$DATA3" ]; then
    #echo "$TIME" | tee -a $LOGPATH/time.log
    #echo "$QUERY1" | tee -a $LOGPATH/kw.log
    #echo "$DATA1" | tee -a $LOGPATH/kw.log
    #echo "$LOG_ENABLE" | tee -a $LOGPATH/log_enable.log
    #echo "$DATA2" | tee -a $LOGPATH/data2.log
    echo "$DATA3" | tee -a $LOGPATH/data2.log
    #echo "$DATA2" | tee -a $LOGPATH/pf.log
    #echo "$DATA3" | tee -a $LOGPATH/current.log
    sleep 3
  #fi
#done

