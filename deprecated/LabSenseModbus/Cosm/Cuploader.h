#include <curl/curl.h>
#include "Cdefs.h"

// Create headers for sending JSON to Cosm
struct curl_slist *createCosmJsonHeaders(CosmConfig *config)
{
    struct curl_slist *headers = NULL;
    char header[128];
    sprintf(header, "X-ApiKey: %s", config->Api_key);
    headers = curl_slist_append(headers, header);
    //headers = curl_slist_append(headers, "Accept: text/plain");
    //headers = curl_slist_append(headers, "Content-type: application/json");
    return headers;
}

// Sends formatted data to Cosm 
int uploadToCosm(char ***data, int count, CosmConfig *config)
{
    CURL *curl;
    CURLcode res;
    char url[URL_LENGTH];
    int i;

    //printf("BEGIN SENDING TO SENSORACT\n");
    //printf("________________________________________________________________\n\n");

    curl = curl_easy_init();
    if(curl) {

        // Format URL
        sprintf(url, "%s%d", config->Url, config->Feed);

        curl_easy_setopt(curl, CURLOPT_URL, url);
        //curl_easy_setopt(curl, CURLOPT_POST, 1);
        //curl_easy_setopt(curl, CURLOPT_PUT, 1);
        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "PUT");
        char *body;

        // Set the headers
        struct curl_slist *headers = createCosmJsonHeaders(config);
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        // Send each body to Cosm 
        for (i = 0; i < count; i++) {
            body = (*data)[i];

            // Set the data in the post message
            curl_easy_setopt(curl, CURLOPT_POSTFIELDS, body);

            /* Perform the request, res will get the return code */ 
            res = curl_easy_perform(curl);

            /* Check for errors */ 
            if(res != CURLE_OK)
                fprintf(stderr, "curl_easy_perform() failed: %s\n",
                        curl_easy_strerror(res));

            // Free memory when done
            free(body);
        }

        /* always cleanup */ 
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);

        //printf("\n\n________________________________________________________________\n");
        //printf("DONE SENDING TO SENSORACT\n");

        return 1;
    }
    else {
        return 0;
    }
    
}

