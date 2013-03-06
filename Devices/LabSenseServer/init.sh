#!/bin/bash

while ! python server.py ../../LabSenseHandler/config.json

do
    sleep 1
    echo "Restarting Program..."
done

