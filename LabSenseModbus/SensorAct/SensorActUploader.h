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

int sendVerisToSensorAct(uint32_t *reg_vals, int count, Type type, time_t timestamp)
{
    char **sa_buf; 
    int i;

    const char IP[] = "http://128.97.93.51:9000/device/list";
    //const int PORT = 9000;
    //const char BODY[] = "{ \"secretkey\": \"2bb5d6b943fc44f0bb6b467450e07ce7\"}";

    // Format data for SensorAct
    if(!sensorActFormatter(&sa_buf, reg_vals, count, type, timestamp))
    {
        SensorActError("Error when formatting data for SensorAct!");
    }

    printf("\nOUTPUT: \n");
    for (i = 0; i < count; i++) {
        printf("%d: %s\n", i, sa_buf[i]);
    }

    // Send formatted data to SensorAct
    if(!sendToSensorAct(&sa_buf, count, IP))
    {
        SensorActError("Error when sending data to SensorAct!");
    }

    return 1;

}

#endif
