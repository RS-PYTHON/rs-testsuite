from behave import given, when, then
from rs_server import rs_server_get, rs_server_post, rs_server_delete
from json_utils import chek_json_path_is_not_null
import json

"""
Fetches the list of collections reachable by the user and filters them based on the user's login.

Parameters:
context (object): An object containing user context, including the login.
headers (dict): A dictionary of HTTP headers to include in the request.

Returns:
list: A list of collections owned by the user.
"""
def get_user_collections(context):
    response = rs_server_get (context, '/catalog/collections')
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
@given('user has deleted all his collections')
def step_remove_user_collections(context):
    # Get the list of the user collection 
    user_collections = get_user_collections(context)
    
    for collection in user_collections:
        url = f"/catalog/collections/{context.login}:{collection['id'][len(context.login)+1:]}"
        rs_server_delete(context, url)

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
    response = rs_server_post(context,'/catalog/collections', collection_json )
    response.raise_for_status() 
    assert(response.status_code == 200)

"""
Count the number of collection owned by the user and check it with the number provided.
"""
@then ('the count of collection should be {number:d}')
def step_check_collection_count(context, number):
    # Get the list of the user collection 
    user_collections = get_user_collections(context)
    count = len(user_collections) 
    assert(count == number), f"Count is {count} and not {number}."
    

"""
Check the queryable interface proposal
"""
@then ('the url /catalog proposes queryables')
def step_check_catalog_queryables(context):
    response = rs_server_get(context, 'catalog/')
    data = json.loads(response.text)
    exists = any(link.get('rel') == 'http://www.opengis.net/def/rel/ogc/1.0/queryables' for link in data.get('links', []))       
    assert (exists == True), "Link http://www.opengis.net/def/rel/ogc/1.0/queryables cannot be found."

"""
Check the queryable interface
"""
@then ('the url catalog/queryables has got 4 properties')
def step_check_catalog_queryables_properties(context):
    response = rs_server_get(context, 'catalog/queryables')
    data = json.loads(response.text)
    chek_json_path_is_not_null(data, 'properties', 'id')
    chek_json_path_is_not_null(data, 'properties', 'datetime')    
    chek_json_path_is_not_null(data, 'properties', 'geometry')
    chek_json_path_is_not_null(data, 'properties', 'eo:cloud_cover')        

"""
Check the queryable interface proposal
"""
@then ('the url /catalog/collections/ for {collection} proposes queryables')
def step_check_collection_queryables(context, collection:str):
    url = f'catalog/collections/{context.login}:{collection}'
    response = rs_server_get(context, url)
    data = json.loads(response.text)
    exists = any(link.get('rel') == 'http://www.opengis.net/def/rel/ogc/1.0/queryables' for link in data.get('links', []))       
    assert (exists == True), f"Link http://www.opengis.net/def/rel/ogc/1.0/queryables cannot be found from url {url}."



"""
Check the queryable interface
"""
@then ('the queryables url for collection {collection} works')
def step_check_queryables(context, collection:str):
    rs_server_get(context, f'catalog/collections/{context.login}:{context.new_collection}/queryables')

