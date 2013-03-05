#!/bin/bash

while ! python server.py 8000

do
    sleep 1
    echo "Restarting Program..."
done

