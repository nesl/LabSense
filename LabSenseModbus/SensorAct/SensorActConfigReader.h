#include <jansson.h>
#include <string.h>

// Read SensorAct config file for Ip, port, and api ke
SensorActConfig *readSensorActConfig()
{
    FILE *fp;
    long lSize;
    char *buffer;
    size_t result;

    int ip_length;
    int api_key_length;

    char IP_CHAR[] = "XXX.XXX.XXX.XXX";
    int PORT;
    char API_KEY_CHAR[] = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";

    // JSON nodes
    json_t *root, *ip, *port, *api_key;
    json_error_t error;

    fp = fopen("../LabSenseConfig/config.json", "r");

    if (fp == NULL) {
        SensorActError("\nCan't open SensorAct Config File!\n");
    }

    // Get File Size
    fseek(fp, 0, SEEK_END);
    lSize = ftell(fp);
    rewind(fp);

    // Allocate memory to contain the whole file
    buffer = (char *) malloc(lSize);
    if(buffer == NULL) {
        SensorActError("\nCould not allocate memory for reading SensorAct Config file!\n");
    }

    // Copy the file into buffer
    result = fread(buffer, 1, lSize, fp);

    if(result != lSize) {
        SensorActError("\nError when reading SensorAct Config File");
    }

    // Read the JSON contents
    root = json_loads(buffer, 0, &error);

    // Free file and buffer
    free(buffer);
    fclose(fp);

    if(!root) {
        SensorActError("\nError when parsing SensorAct Config File");
    }

    // Get IP, Port, and API_KEY
    ip = json_object_get(root, "IP");
    port = json_object_get(root, "PORT");
    api_key = json_object_get(root, "API_KEY");

    // Get values
    strcpy(IP_CHAR, json_string_value(ip));
    strcpy(API_KEY_CHAR, json_string_value(api_key));

    // Allocate memory for config
    SensorActConfig *config = malloc(sizeof(SensorActConfig*));

    ip_length = strlen(IP_CHAR);
    api_key_length = strlen(API_KEY_CHAR);

    // IP length + 1 for NULL
    config->Ip = (char *) malloc(ip_length + 1);
    // API key length + 1 for NULL
    config->Api_key = (char *) malloc(api_key_length + 1);

    if(!config->Ip || !config->Api_key)
    {
        SensorActError("Can't allocate memory for SensorAct Configuration");
    }

    strcpy(config->Ip, IP_CHAR);
    strcpy(config->Api_key, API_KEY_CHAR);
    config->Port = json_integer_value(port);

    return config;

}
