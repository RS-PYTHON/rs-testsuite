"""STAC Catalog test steps"""

from behave import given, when, then
import os
import requests
from urllib.parse import urljoin
import json

# Perform a Get call to the catalog and send back the response
def catalog_get(context, url:str)-> str:
    assert context.apikey is not None
    assert os.getenv("STAC_API_URL") is not None
    
    # Push API-KEY on the header
    headers = {"x-api-key": f"{context.apikey}"}

    
    with requests.Session() as session:
        response = session.get(os.getenv("STAC_API_URL") + url, headers=headers)
        response.raise_for_status() 
        assert(response.status_code == 200)
        return response


# Perform a POST call to the catalog and send back the response
def catalog_post(context, url:str, parameter:json)-> str:
    assert context.apikey is not None
    assert os.getenv("STAC_API_URL") is not None
    
    # Push API-KEY on the header
    headers = {"x-api-key": f"{context.apikey}"}

    with requests.Session() as session:
        response = session.post(os.getenv("STAC_API_URL") + url, data=json.dumps(parameter), headers=headers)
        response.raise_for_status() 
        assert(response.status_code == 200)
        return response


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

"""
Fetches the list of collections reachable by the user and filters them based on the user's login.

Parameters:
context (object): An object containing user context, including the login.
headers (dict): A dictionary of HTTP headers to include in the request.

Returns:
list: A list of collections owned by the user.
"""
def get_user_collections(context):
    response = catalog_get (context, '/catalog/collections')
    collections = response.json()['collections']
        
    # Remove duplicates from the collections list
    collections_without_duplicate = []
    for item in collections:
        if item not in collections_without_duplicate:
            collections_without_duplicate.append(item)

    # Filter collections to extract those owned by the user
    user_collections = [collection for collection in collections_without_duplicate if collection['id'].startswith(context.login)]
    
    return user_collections

"""
Delete all the Collection from one user.
"""    
@given('user {user:d} has deleted all his collections')
def step_remove_user_collections(context, user: int):
    assert context.apikey is not None
    # Push API-KEY on the header
    headers = {"x-api-key": f"{context.apikey}"}

    # Get the list of the user collection 
    user_collections = get_user_collections(context)
    
    with requests.Session() as session:
        # Delete all collection owned by the user
        for collection in user_collections:
            response = session.delete(urljoin(os.getenv("STAC_API_URL"),
                    f'/catalog/collections/{context.login}:{collection['id'][len(context.login)+1:]}'),
                    headers=headers)
            response.raise_for_status() 
            assert(response.status_code == 200)

"""
Create a single collection with fake description.
"""
@given('the collection "{name}" is created')
@when ('the collection "{name}" is created')
def step_create_collection(context, name):
    context.new_collection = name
    collection_json = {
            "id": f"{name}",
            "type": "Collection",
            "description": f"{name} default description",
            "stac_version": "1.0.0",            
            "owner": f"{context.login}",
        }
    # Call the endpoint to create the collection
    response = catalog_post(context,'/catalog/collections', collection_json )

"""
Count the number of collection owned by the user and check it with the number provided.
"""
@then ('the count of collection should be {number:d}')
def step_check_collection_count(context, number):
    # Get the list of the user collection 
    user_collections = get_user_collections(context)
    assert(len(user_collections) == number)
    

"""
Check the queryable interface proposal
"""
@then ('the url /catalog proposes queryables')
def step_check_queryables(context):
    response = catalog_get(context, 'catalog/')
    data = json.loads(response.text)
    exists = any(link.get('rel') == 'http://www.opengis.net/def/rel/ogc/1.0/queryables' for link in data.get('links', []))       
    assert (exists == True)

"""
Check the queryable interface
"""
@then ('the url catalog/queryables has got 4 properties')
def step_check_queryables(context):
    response = catalog_get(context, 'catalog/queryables')
    data = json.loads(response.text)
    assert (data['properties']['id'] is not None)
    assert (data['properties']['datetime'] is not None)
    assert (data['properties']['geometry'] is not None)
    assert (data['properties']['eo:cloud_cover'] is not None)            



"""
Check the queryable interface
"""
@then ('the queryables url for collection {collection} works')
def step_check_queryables(context, collection:str):
    response = catalog_get(context, f'catalog/collections/{context.login}:{context.new_collection}/queryables')
    data = json.loads(response.text)
