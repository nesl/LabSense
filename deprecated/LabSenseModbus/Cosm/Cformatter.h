#include "Cdefs.h"
#include "../SensorAct/defs.h"
#include <stdint.h>
#include <string.h>

// Converts the register values into SensorAct format
// Returns array of strings to send to SensorAct
int cosmFormatter(char ***sa_buf, uint32_t *reg_vals, int *count, Type type, char *api_key)
{
    char in_buf[4096];
    char line_buf[256];
    char id[64];
    int i;
    int retVal;

    if(type == Eaton) {

        strcpy(in_buf, "{ \"version\":\"1.0.0\",\
                \"datastreams\": [");

        for (i = 0; i < *count; i++) {
            if(i < 3) {
                strcpy(id, "Voltage");
            }
            else if(i < 6) {
                strcpy(id, "Current");
            }
            else if(i < 9) {
                strcpy(id, "Power");
            }
            else if(i < 12) {
                strcpy(id, "VARs");
            }
            else if(i < 15) {
                strcpy(id, "VAs");
            }
            else if(i < 18) {
                strcpy(id, "PowerFactor");
            }

            sprintf(line_buf, "{\"id\": \"Phase%c%s\", \"current_value\":\"%f\"},", ((i %3) + 'A'), id, *(float*)(&reg_vals[i]));
            strcat(in_buf, line_buf);
        }

        // Remove trailing comma
        in_buf[strlen(in_buf)-1] = '\0';

        // Append ending brackets
        strcat(in_buf, "]}");

        // SensorAct buffer initialization
        *sa_buf = (char **) malloc((*count)*sizeof(char*));

        (*sa_buf)[0] = malloc(COSM_BUFFER_LENGTH);
        strcpy((*sa_buf)[0], in_buf);

        // Only one message to send to COSM
        *count = 1;

        retVal = 1;
    }
    else {
        retVal = 0;
    }

    return retVal;
}
