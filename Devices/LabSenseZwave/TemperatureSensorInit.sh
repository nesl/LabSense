#!/bin/bash

while ! python ZwaveDevice.py ../../LabSenseHandler/config.json TemperatureSensor 

do
    sleep 1
    echo "Restarting Program..."
done

