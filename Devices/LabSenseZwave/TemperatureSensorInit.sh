#!/bin/bash

while ! python ZwaveDevice.py NESL_TempSensor TemperatureSensor 172.17.5.117 3480 2

do
    sleep 1
    echo "Restarting Program..."
done

