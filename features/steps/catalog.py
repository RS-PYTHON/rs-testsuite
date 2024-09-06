"""STAC Catalog test steps"""

from behave import given, when, then
from behave import use_step_matcher

import os
import requests
import uuid
import json
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.parse import urljoin


"""
Step to ensure that the API-KEY is set on environment variable.
We will avoid to create an API-KEY for each test.
There is a dedicated test to check API-KEY creation.
"""

@given('user {user:d} has got an apikey')
def step_check_apikey(context, user: int):
    """Checks that user APIKEY is set on environment variable"""
    assert f'RSPY_TEST_APIK_{user}' in os.environ
    context.apikey = os.getenv(f'RSPY_TEST_APIK_{user}')


import os
import requests
from urllib.parse import urljoin

def get_user_collections(context, headers):
    """
    Fetches the list of collections reachable by the user and filters them based on the user's login.

    Parameters:
    context (object): An object containing user context, including the login.
    headers (dict): A dictionary of HTTP headers to include in the request.

    Returns:
    list: A list of collections owned by the user.
    """
    with requests.Session() as session:
        # Perform an HTTP GET request to fetch collections
        response = session.get(urljoin(os.getenv("STAC_API_URL"), '/catalog/collections'), headers=headers)
        response.raise_for_status()
        assert(response.status_code == 200)
        collections = response.json()['collections']
        
        # Remove duplicates from the collections list
        collections_without_duplicate = []
        for item in collections:
            if item not in collections_without_duplicate:
                collections_without_duplicate.append(item)

        # Print the unfiltered list of collections
        #print("List of STAC Collections reachable by the user (unfiltered):")
        #for collection in collections_without_duplicate:
            #print(f"ID: {collection['id']}, Title: {collection['owner']}")

        # Filter collections to extract those owned by the user
        user_collections = [collection for collection in collections_without_duplicate if collection['id'].startswith(context.login)]
        
        return user_collections


    

@given('user {user:d} has deleted all his collections')
def step_remove_user_collections(context, user: int):
    """
    Clean the Collection from one user.
    """    
    # Push API-KEY on the header
    headers = {"x-api-key": f"{context.apikey}"}

    # Get the list of the user collection 
    user_collections = get_user_collections(context, headers)
    
    with requests.Session() as session:
        # Delete all collection owned by the user
        for collection in user_collections:
            #print(f"ID: {collection['id']}, Title: {collection['owner']}, Title filtered {collection['id'][len(context.login)+1:]} to be deleted.")
            response = session.delete(urljoin(os.getenv("STAC_API_URL"),
                    f'/catalog/collections/{context.login}:{collection['id'][len(context.login)+1:]}'),
                    headers=headers)
            response.raise_for_status() 
            assert(response.status_code == 200)
            
    


@given('He creates the collection "{name}"')
@when ('He creates the collection "{name}"')
def step_create_collection(context, name):
    """
    Create a single collection with fake description.
    """
    # Push API-KEY on the header
    headers = {"x-api-key": f"{context.apikey}"}
    context.new_collection = name
        
    collection_json = {
            "id": f"{name}",
            "type": "Collection",
            "description": f"{name} default description",
            "stac_version": "1.0.0",            
            "owner": f"{context.login}",
        }
    #print (json.dumps(collection_json, indent=4))
    # Call the endpoint to create the collection
    with requests.Session() as session:
        url = urljoin(os.getenv("STAC_API_URL"), '/catalog/collections')
        response = session.post(url, data=json.dumps(collection_json),headers=headers)        
        response.raise_for_status() 
        assert(response.status_code == 200)        
    #print()


@then ('The count of collection is {number:d}')
def step_check_collection_count(context, number):
    """
    Count the number of collection owned by the user and check it with the number provided.
    """
    # Push API-KEY on the header
    headers = {"x-api-key": f"{context.apikey}"}
    
    # Get the list of the user collection 
    user_collections = get_user_collections(context, headers)
    assert(len(user_collections) == number)
    