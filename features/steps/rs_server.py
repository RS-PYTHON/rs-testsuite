import os
import requests
import json

# Perform a Get call to the catalog and send back the response
def rs_server_get(context, url:str, status:int=200)-> str:
    assert context.apikey is not None, "API-KEY is not set."
    assert os.getenv("STAC_API_URL") is not None, "STAC_API_URL is not set."
    
    # Push API-KEY on the header
    headers = {"x-api-key": f"{context.apikey}"}

    
    with requests.Session() as session:
        response = session.get(os.getenv("STAC_API_URL") + url, headers=headers)
        assert(response.status_code == status), f'status for GET {url} is {response.status_code} and not {status}'
        return response


# Perform a POST call to the catalog and send back the response
def rs_server_post(context, url:str, parameter:json, status:int=200)-> str:
    assert context.apikey is not None, "API-KEY is not set."
    assert os.getenv("STAC_API_URL") is not None, "STAC_API_URL is not set."
    
    # Push API-KEY on the header
    headers = {"x-api-key": f"{context.apikey}"}

    with requests.Session() as session:
        response = session.post(os.getenv("STAC_API_URL") + url, data=json.dumps(parameter), headers=headers)
        assert(response.status_code == status), f'status for POST {url} is {response.status_code} and not {status}'
        return response
    
def rs_server_delete(context, url:str, status:int=200) ->str:
    assert context.apikey is not None, "API-KEY is not set."
    assert os.getenv("STAC_API_URL") is not None, "STAC_API_URL is not set." 
    # Push API-KEY on the header
    headers = {"x-api-key": f"{context.apikey}"}

    
    with requests.Session() as session:
        response = session.delete(os.getenv("STAC_API_URL") + url, headers=headers)
        response.raise_for_status() 
        assert(response.status_code == status), f'status for DELETE {url} is {response.status_code} and not {status}'
