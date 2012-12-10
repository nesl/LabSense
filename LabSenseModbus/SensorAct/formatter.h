#include "defs.h"
#include <stdint.h>
#include <string.h>

// Converts the register values into SensorAct format
// Returns array of strings to send to SensorAct
int sensorActFormatter(char ***sa_buf, uint32_t *reg_vals, int count, Type type, time_t timestamp)
{
    // Use large buffer to store JSON
    char buffer[SENSORACT_BUFFER_SIZE];

    char dname[10];
    char cname[10];
    char unit[10];
    int retVal;
    int i;

    // SensorAct buffer initialization
    *sa_buf = (char **) malloc(count*sizeof(char*));

    char in_buf[] = 
    "{ \"secretkey\": \"%s\", \
        \"data\": { \
            \"dname\": \"%s\", \
            \"sname\": \"Outlet%d\", \
            \"sid\": \"%d\", \
            \"sinterval\": \"1\", \
            \"timestamp\": %i, \
            \"loc\": \"BH1762/UCLA\", \
            \"channels\": [ { \
                \"cname\": \"%s\", \
                \"unit\": \"%s\", \
                \"readings\": [ %f\
                ] \
            } ] \
        } \
    }";

    if(type == VerisPower || type == VerisPowerFactor || type == VerisCurrent)
    {
        strcpy(dname, "NESL_Veris");

        if(type == VerisPower) 
        {
            strcpy(cname, "Power");
            strcpy(unit, "kW");
        }
        else if(type == VerisPowerFactor)
        {
            strcpy(cname, "Power Factor");
            strcpy(unit, "%");
        }
        else if(type == VerisCurrent)
        {
            strcpy(cname, "Current");
            strcpy(unit, "A");
        }

        for (i = 0; i < count; i++) {
            sprintf(buffer, in_buf, "2bb5d6b943fc44f0bb6b467450e07ce7", dname, i+1, i+1, timestamp, cname, unit, *(float*)(&reg_vals[i]));
            (*sa_buf)[i] = malloc(SENSORACT_BUFFER_SIZE);
            strcpy((*sa_buf)[i], buffer);
            //printf("\nOUTPUT STRING: %s\n", buffer);
            //printf("\nOUTPUT STRING: %s\n", (*sa_buf)[i]);
        }

        retVal = 1;

    }
    else if(type == Eaton)
    {
        strcpy(dname, "Eaton");
        retVal = 1;
    }
    else {
        retVal = 0;
    }

    return retVal;
}
