#!/bin/bash

while ! python SmartSwitchZwaveDevice.py NESL_SmartSwitch 172.17.5.117 3480 2

do
    sleep 1
    echo "Restarting Program..."
done

