#!/bin/bash

while ! python VerisDevice.py NESL_Veris 128.97.93.90 4660 1

do
    sleep 1
    echo "Restarting Program..."
done

