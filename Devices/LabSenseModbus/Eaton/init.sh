#!/bin/bash

while ! python EatonDevice.py ../../../LabSenseHandler/config.json

do
    sleep 1
    echo "Restarting Program..."
done

