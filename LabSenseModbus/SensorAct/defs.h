#ifndef DEFS_H
#define DEFS_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SENSORACT_BUFFER_SIZE 1024
#define URL_LENGTH 128

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
    fprintf(stderr, "%s", str);
    fprintf(stderr, "%s", "Exiting...");
    exit(1);
}

typedef struct SensorActConfig {
    char *Ip;
    int Port;
    char *Api_key;
} SensorActConfig;

#endif
