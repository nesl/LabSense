#!/bin/bash

while ! python EatonDevice.py ../../../LabSenseHandler/config.json NESL_Eaton

do
    sleep 1
    echo "Restarting Program..."
done

