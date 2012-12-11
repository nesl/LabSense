#ifndef SENSORACT_H
#define SENSORACT_H

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/time.h>

#include "uploader.h"
#include "formatter.h"
#include "defs.h"
#include "SensorActConfigReader.h"


// Send Veris data to SensorAct
int sendToSensorAct(uint32_t *reg_vals, int count, Type type, time_t timestamp)
{
    char **sa_buf; 
    int i;

    SensorActConfig *config;
    config = readSensorActConfig();

    // Format data for SensorAct
    if(!sensorActFormatter(&sa_buf, reg_vals, &count, type, timestamp, config->Api_key))
    {
        SensorActError("Error when formatting data for SensorAct!");
    }

    // Send formatted data to SensorAct
    if(!uploadToSensorAct(&sa_buf, count, config))
    {
        SensorActError("Error when sending data to SensorAct!");
    }
    else {
        printf("\nSuccessfully Sent Data to SensorAct!\n\n");
    }

    return 1;

}

#endif
