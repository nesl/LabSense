#!/bin/bash

while ! python ZwaveDevice.py ../../LabSenseHandler/config.json LightSensor NESL_LightSensor

do
    sleep 1
    echo "Restarting Program..."
done

