#include <jansson.h>
#include <string.h>

// Read Cosm config file for Ip, port, and api ke
CosmConfig *readCosmConfig()
{
    int url_length;
    int api_key_length;

    char URL_CHAR[128];
    char API_KEY_CHAR[128];

    // JSON nodes
    json_t *root, *url, *json_feed, *api_key;
    json_error_t error;

    // Read the JSON contents
    root = json_load_file("Cosm/config.json", 0, &error);

    if(!root) {
        CosmError("\nError when parsing Cosm Config File");
    }

    // Get url, Feed, and API_KEY
    url = json_object_get(root, "URL");
    json_feed = json_object_get(root, "feed");
    api_key = json_object_get(root, "API_KEY");

    // Get values
    strcpy(URL_CHAR, json_string_value(url));
    strcpy(API_KEY_CHAR, json_string_value(api_key));

    // Free json objects
    free(root);
    free(url);
    free(api_key);

    // Allocate memory for config
    CosmConfig *config = malloc(sizeof(CosmConfig *));

    url_length = strlen(URL_CHAR);
    api_key_length = strlen(API_KEY_CHAR);


    // url length + 1 for NULL
    config->Url = (char *) malloc(url_length + 1);
    // API key length + 1 for NULL
    config->Api_key = (char *) malloc(api_key_length + 1);

    if(!config->Url || !config->Api_key)
    {
        CosmError("Can't allocate memory for Cosm Configuration");
    }

    strcpy(config->Url, URL_CHAR);
    strcpy(config->Api_key, API_KEY_CHAR);
    config->Feed = json_integer_value(json_feed);

    return config;

}
