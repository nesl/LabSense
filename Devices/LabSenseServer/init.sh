#!/bin/bash

while ! python server.py ../../LabSenseHandler/config.json NESL_LabSenseServer

do
    sleep 1
    echo "Restarting Program..."
done

