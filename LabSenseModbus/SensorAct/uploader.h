#include <curl/curl.h>

// Create headers for sending JSON to SensorAct
struct curl_slist *createJsonHeaders()
{
    struct curl_slist *headers = NULL;
    headers = curl_slist_append(headers, "Accept: text/plain");
    headers = curl_slist_append(headers, "Content-type: application/json");
    return headers;
}

// Sends formatted data to SensorAct
int sendToSensorAct(char ***data, int count, const char *ip)
{
    CURL *curl;
    CURLcode res;
    int i;

    printf("BEGIN SENDING TO SENSORACT\n");
    printf("________________________________________________________________\n\n");

    curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, ip);
        curl_easy_setopt(curl, CURLOPT_POST, 1);
        char *body;

        // Set the headers
        struct curl_slist *headers = createJsonHeaders();
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        // Send each body to SensorAct
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



        printf("\n\n________________________________________________________________\n");
        printf("DONE SENDING TO SENSORACT\n");

        return 1;
    }
    else {
        return 0;
    }
    
}

