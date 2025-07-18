import json

from behave import given, then, when
from json_utils import check_json_path_is_not_null
from rs_server import rs_server_delete, rs_server_get, rs_server_post


def get_user_collections(context):
    """
    Fetches the list of collections reachable by the user and filters them based on the user's login.

    Parameters:
    context (object): An object containing user context, including the login.
    headers (dict): A dictionary of HTTP headers to include in the request.

    Returns:
    list: A list of collections owned by the user.
    """
    assert (
        context.login is not None
    ), "Login has not be added to the set on the request header."
    response = rs_server_get(context, "/catalog/collections", 200)
    collections = response.json()["collections"]

    # Remove duplicates from the collections list
    collections_without_duplicate = []
    for item in collections:
        if item not in collections_without_duplicate:
            collections_without_duplicate.append(item)

    # Filter collections to extract those owned by the user
    user_collections = [
        collection
        for collection in collections_without_duplicate
        if collection["id"].startswith(context.login)
    ]

    return user_collections


@given("user has deleted all his collections")
def step_remove_user_collections(context):
    """
    Delete all the Collection from one user.
    """
    assert (
        context.login is not None
    ), "Login has not be added to the set on the request header."
    assert (
        context.apikey is not None
    ), "apikey has not be added to the set on the request header."

    # Get the list of the user collection
    user_collections = get_user_collections(context)

    for collection in user_collections:
        url = f"/catalog/collections/{context.login}:{collection['id'][len(context.login)+1:]}"
        rs_server_delete(context, url)


@given('the collection "{name}" is created')
@when('the collection "{name}" is created')
def step_create_collection(context, name):
    """
    Create a single collection with fake description.
    """
    assert (
        context.login is not None
    ), "Login has not be added to the set on the request header."
    context.new_collection = name

    collection_json = {
        "id": f"{name}",
        "type": "Collection",
        "links": [],
        "owner": f"{context.login}",
        "extent": {
            "spatial": {"bbox": [[-180, -90, 180, 90]]},
            "temporal": {
                "interval": [["2000-01-01T00:00:00Z", "2030-01-01T00:00:00Z"]],
            },
        },
        "license": "public-domain",
        "description": f"{name} default description",
        "stac_version": "1.0.0",
    }

    # Call the endpoint to create the collection
    rs_server_post(context, "/catalog/collections", collection_json, 201)


@then("the count of collection should be {number:d}")
def step_check_collection_count(context, number):
    """
    Count the number of collection owned by the user and check it with the number provided.
    """
    # Get the list of the user collection
    user_collections = get_user_collections(context)
    count = len(user_collections)
    assert count == number, f"Count is {count} and not {number}."


@then("the url /catalog proposes queryables")
def step_check_catalog_queryables(context):
    """
    Check the queryable interface proposal
    """
    response = rs_server_get(context, "catalog/", 200)
    data = json.loads(response.text)
    exists = any(
        link.get("rel") == "http://www.opengis.net/def/rel/ogc/1.0/queryables"
        for link in data.get("links", [])
    )
    assert (
        exists is True
    ), "Link http://www.opengis.net/def/rel/ogc/1.0/queryables cannot be found."


@then("the url catalog/queryables has got 3 properties")
def step_check_catalog_queryables_properties(context):
    """
    Check the queryable interface
    """
    response = rs_server_get(context, "catalog/queryables", 200)
    data = json.loads(response.text)
    check_json_path_is_not_null(data, "properties", "id")
    check_json_path_is_not_null(data, "properties", "datetime")
    check_json_path_is_not_null(data, "properties", "geometry")


@then("the url /catalog/collections/ for {collection} proposes queryables")
def step_check_collection_queryables(context, collection: str):
    """
    Check the queryable interface proposal
    """
    assert (
        context.login is not None
    ), "Login has not be added to the set on the request header."
    url = f"catalog/collections/{context.login}:{collection}"
    response = rs_server_get(context, url)
    data = json.loads(response.text)
    exists = any(
        link.get("rel") == "http://www.opengis.net/def/rel/ogc/1.0/queryables"
        for link in data.get("links", [])
    )
    assert (
        exists is True
    ), f"Link http://www.opengis.net/def/rel/ogc/1.0/queryables cannot be found from url {url}."


@then("the queryables url for collection {collection} works")
def step_check_queryables(context, collection: str):
    """
    Check the queryable interface
    """
    assert (
        context.login is not None
    ), "Login has not be added to the set on the request header."
    rs_server_get(
        context,
        f"catalog/collections/{context.login}:{collection}/queryables",
    )
