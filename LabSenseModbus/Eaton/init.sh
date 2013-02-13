#!/bin/bash

while ! python EatonDevice.py NESL_Eaton 128.97.11.100 4660 1

do
    sleep 1
    echo "Restarting Program..."
done

