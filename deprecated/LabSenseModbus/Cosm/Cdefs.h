#ifndef CDEFS_H
#define CDEFS_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COSM_BUFFER_LENGTH 2048
#define URL_LENGTH 128

int CosmError(char *str)
{
    fprintf(stderr, "%s\n", str);
    fprintf(stderr, "%s\n", "Exiting...");
    exit(1);
}

typedef struct CosmConfig {
    char *Url;
    int Feed;
    char *Api_key;
} CosmConfig;

void freeCosmConfig(CosmConfig *config) {
    free(config->Url);
    free(config->Api_key);
    free(config);
}

#endif
