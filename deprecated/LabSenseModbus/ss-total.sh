#!/bin/bash

LOGPATH=$1
if [ -z "$LOGPATH" ]; then
  LOGPATH=log1
else
  mkdir $LOGPATH
fi

while [ 1 ]; do 
  TIME=`date +%s`
  
  DATA1=`./TCPModbusClient r 172.17.5.178 4660 1 619 12 2>&1 | grep -A 1 float | grep "\."`
  if [ -n "$DATA1" ]; then
    echo "$TIME" | tee -a $LOGPATH/time.log
    echo "$DATA1" | tee -a $LOGPATH/kw.log
    sleep 1.5
  fi
done

