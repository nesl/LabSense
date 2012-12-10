#ifndef DEFS_H
#define DEFS_H

#include <stdio.h>
#include <stdlib.h>

#define SENSORACT_BUFFER_SIZE 1024

// This enum is used specifically for the zeromq_special_mode.
typedef enum Type {
    Normal = 0, // This is the default type,where the zeromq_special_mode is 
                // not used.
    Eaton,
    VerisPower,      // This is for getting power in zeromq_special_mode.
    VerisPowerFactor,// This is for getting power factor in zeromq_special_mode.
    VerisCurrent     // This is for getting current in zeromq_special_mode.
} Type;


int SensorActError(char *str)
{
    printf("%s", str);
    printf("Exiting...");
    exit(1);
}

#endif
