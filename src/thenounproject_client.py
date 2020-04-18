#!/usr/bin/env python

#
# this is the example client from the openapi generator
#

from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint


# Defining host is optional and default to http://api.thenounproject.com
configuration.host = "http://api.thenounproject.com"
# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.CollectionApi(api_client)
    id = 56 # int | Collection id

    try:
        # Get collection by id
        api_instance.get_collection_by_id(id)
    except ApiException as e:
        print("Exception when calling CollectionApi->get_collection_by_id: %s\n" % e)
    