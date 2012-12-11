#include "defs.h"
#include <stdint.h>
#include <string.h>

// Converts the register values into SensorAct format
// Returns array of strings to send to SensorAct
int sensorActFormatter(char ***sa_buf, uint32_t *reg_vals, int *count, Type type, time_t timestamp, char *api_key)
{
    // Use large buffer to store JSON
    char buffer[SENSORACT_BUFFER_SIZE];

    char dname[10];
    char cname[10];
    char unit[10];
    char in_buf[1024]; 
    char channel_buf[SENSORACT_CHANNEL_BUF_SIZE];
    char sa_channel_generic[SENSORACT_CHANNEL_BUF_SIZE];
    const char *channels[] = {"Voltage", "Current", "Power", "VARs", "VAs", "Power Factor"};
    const char *chan_units[] = {"Volts", "Amps", "Watts", "VARs", "VAs", "None"};
    char sensorActChannels[EATON_NUM_CHANNELS][SENSORACT_CHANNEL_BUF_SIZE];
    int retVal;
    int i, j;

    // SensorAct buffer initialization
    *sa_buf = (char **) malloc((*count)*sizeof(char*));

    if(type == VerisPower || type == VerisPowerFactor || type == VerisCurrent)
    {
        
        strcpy(in_buf, "{ \"secretkey\": \"%s\", \
            \"data\": { \
                \"dname\": \"%s\", \
                \"sname\": \"%s%d\", \
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
        }");

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

        for (i = 0; i < *count; i++) {
            sprintf(buffer, in_buf, api_key, dname, "Outlet", i+1, i+1, timestamp, cname, unit, *(float*)(&reg_vals[i]));
            (*sa_buf)[i] = malloc(SENSORACT_BUFFER_SIZE);
            strcpy((*sa_buf)[i], buffer);
        }

        retVal = 1;

    }
    else if(type == Eaton)
    {

        // Generic SensorAct data representation
        strcpy(in_buf, "{ \"secretkey\": \"%s\", \
            \"data\": { \
                \"dname\": \"%s\", \
                \"sname\": \"%s%c\", \
                \"sid\": \"%d\", \
                \"sinterval\": \"1\", \
                \"timestamp\": %i, \
                \"loc\": \"BH1762/UCLA\", \
                \"channels\": [");

        // Generic channel representation
        strcpy(sa_channel_generic, 
        "{\
           \"cname\": \"%s\", \
           \"unit\": \"%s\", \
           \"readings\": [ %f\
          ]\
        },");

        strcpy(dname, "NESL_Eaton");

        // Copy data into JSON
        for (i = 0; i < EATON_NUM_PHASES; i++) {
            sprintf(buffer, in_buf, api_key, dname, "Phase", i + 'A', i+1, timestamp);

            for (j = 0; j < EATON_NUM_CHANNELS; j++) {
                strcpy(cname, channels[j]);
                strcpy(unit, chan_units[j]);
                sprintf(channel_buf, sa_channel_generic, channels[j], chan_units[j], *(float*)(&reg_vals[i + j*EATON_NUM_PHASES]));
                strcat(buffer, channel_buf); 
            }

            // Remove trailing comma of end channel
            buffer[strlen(buffer)-1] = '\0';

            // Append the finishing brackets
            strcat(buffer, "]}}");

            (*sa_buf)[i] = malloc(SENSORACT_BUFFER_SIZE);
            strcpy((*sa_buf)[i], buffer);

            printf("OUTPUT %d: %s\n\n", i, (*sa_buf)[i]);
        }

        // Change the count to 3 because there are three total messages that
        // should be uploaded to SensorAct
        *count = EATON_NUM_PHASES;

        retVal = 1;
    }
    else {
        retVal = 0;
    }

    return retVal;
}
