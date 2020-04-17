#!/usr/bin/env python

from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

configuration = openapi_client.Configuration()
# Configure API key authorization: apiKeyHeader
configuration.api_key['api_key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'
configuration = openapi_client.Configuration()
# Configure API key authorization: apiKeyQuery
configuration.api_key['api_key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Defining host is optional and default to http://api.wmata.com/Rail.svc
configuration.host = "http://localhost/Rail.svc"
# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    
    try:
        # JSON - Lines
        api_instance.call_5476364f031f5909e4fe330c()
    except ApiException as e:
        print("Exception when calling DefaultApi->call_5476364f031f5909e4fe330c: %s\n" % e)
    