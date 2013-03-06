#!/bin/bash

while ! python ZwaveDevice.py ../../LabSenseHandler/config.json LightSensor

do
    sleep 1
    echo "Restarting Program..."
done

