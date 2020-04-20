#!/usr/bin/env python

#
# this is the example client from the openapi generator
#

from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint


# Defining host is optional and default to https://localhost/api/v1
configuration = openapi_client.Configuration()
configuration.host = "http://pyserver:8080/api/v1"
# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    
    try:
        api_response = api_instance.cart_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->cart_get: %s\n" % e)

