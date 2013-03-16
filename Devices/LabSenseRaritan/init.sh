#!/bin/bash

# Usage:
# python RaritanDevice [Raritan_Name] [Raritan_IP] [Raritan_PORT] [Sample_interval]

#while ! python RaritanDevice.py NESL_Raritan 172.17.5.179 161 1
while ! python RaritanDevice.py ../../LabSenseHandler/config.json NESL_Raritan

do
    sleep 1
    echo "Restarting Program..."
done

