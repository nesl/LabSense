#!/bin/bash

while ! python ZwaveDevice.py ../../LabSenseHandler/config.json TemperatureSensor NESL_TempSensor

do
    sleep 1
    echo "Restarting Program..."
done

