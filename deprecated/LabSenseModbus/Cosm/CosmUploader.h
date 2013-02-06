#ifndef COSM_H 
#define COSM_H 

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/time.h>

#include "Cuploader.h"
#include "Cformatter.h"
#include "Cdefs.h"
#include "CosmConfigReader.h"

// Send Veris data to Cosm
int sendToCosm(uint32_t *reg_vals, int count, Type type)
{
    char **sa_buf; 
    int i;

    CosmConfig *config;
    config = readCosmConfig();

    // Format data for Cosm
    if(!cosmFormatter(&sa_buf, reg_vals, &count, type, config->Api_key))
    {
        CosmError("Error when formatting data for Cosm!");
    }

    // Send formatted data to Cosm
    if(!uploadToCosm(&sa_buf, count, config))
    {
        CosmError("Error when sending data to Cosm!");
    }
    else {
        printf("\nSuccessfully Sent Data to Cosm!\n");
    }

    // Free memory
    freeCosmConfig(config);
    free(sa_buf);

    return 1;

}

#endif
