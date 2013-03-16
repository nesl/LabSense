#!/bin/bash

while ! python ZwaveDevice.py ../../LabSenseHandler/config.json SmartSwitch NESL_SmartSwitch

do
    sleep 1
    echo "Restarting Program..."
done

