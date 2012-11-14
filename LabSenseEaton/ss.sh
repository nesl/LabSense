while [ 1 ]
do 
./TCPModbusClient r 172.17.5.178 4660 1 1251 42
sleep 3
done
