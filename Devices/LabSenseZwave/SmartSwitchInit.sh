#!/bin/bash

while ! python ZwaveDevice.py ../../LabSenseHandler/config.json SmartSwitch

do
    sleep 1
    echo "Restarting Program..."
done

