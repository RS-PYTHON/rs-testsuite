from behave import given, when, then
from behave import use_step_matcher
from pystac import Collection, Item
from pystac_client import Client
from rs_client.rs_client import RsClient
from stac_api_validator.validations import QueryConfig
from stac_api_validator.validations import validate_api

import logging
import os


logger = logging.getLogger(__name__)


use_step_matcher("re")


@given('the (?P<stac_instance>CATALOG|CADIP|AUXIP|LTA|PRIP) STAC API')
def step_given_stac_api(context, stac_instance: str):
    for url in ['STAC_API_URL', 'CADIP_STAC_API_URL', 'AUXIP_STAC_API_URL', 'LTA_STAC_API_URL', 'PRIP_STAC_API_URL']:
        assert os.getenv(url) is not None, url + " is not set."
    context.stac_api_root_url = os.environ[{
                'CATALOG': 'STAC_API_URL',
                'CADIP': 'CADIP_STAC_API_URL',
                'AUXIP': 'AUXIP_STAC_API_URL',
                'LTA': 'LTA_STAC_API_URL',
                'PRIP': 'PRIP_STAC_API_URL'
                }[stac_instance]]


use_step_matcher("parse")


@given('a set of STAC conformance classes')
def step_given_stac_conformance_classes(context):
    context.stac_conformance_classes = []
    for row in context.table:
        context.stac_conformance_classes.append(row['class'])


@given('the bbox {bbox}')
def step_given_stac_bbox(context, bbox: list[float]):
    context.stac_geometry = bbox


@given('the collection "{collection}" exists')
def step_given_stac_collection_exists(context, collection: str):
    context.stac_collection = collection
    step_given_stac_collections_exist(context, collection)


@then('the collection "{collection}" exists')
def step_then_stac_collection_exists(context, collection: str):
    step_then_stac_collections_exist(context, collection)


@given('the collections "{collections}" exist')
def step_given_stac_collections_exist(context, collections: str):
    context.stac_collection = collections
    assert_stac_collections_exist(context, collections)


@then('the collections "{collections}" exist')
def step_then_stac_collections_exist(context, collections: str):
    assert_stac_collections_exist(context, collections)


def assert_stac_collections_exist(context, collections: str):
    assert do_stac_collections_exist(context, collections), \
        f"No expected count of collections found for {collections}"


@given('the collection "{collection}" does not exist')
def step_given_stac_collection_does_not_exist(context, collection: str):
    context.stac_collection = collection
    step_given_stac_collections_do_not_exist(context, collection)


@given('the collections "{collections}" do not exist')
def step_given_stac_collections_do_not_exist(context, collections: str):
    context.stac_collections = collections
    assert not do_stac_collections_exist(context, collections), \
        f"No expected count of collections found for {collections}"


def do_stac_collections_exist(context, collections: str) -> bool:
    collection_ids = collections.split(',')

    context.stac_collections = []
    for collection_id in collection_ids:
        context.stac_collections.append(collection_id)
        # Explicit prefixing needed for some tests because search by implicit naming does not work
#        if (os.environ['USER'] not in collection_id):
#            context.stac_collections.append(os.environ['USER'] + '_' + collection_id)

    found_collections = create_pystac_client(context).get_collections()
    assert found_collections is not None, f"No collections found for {collections}"
    matches = 0
    for id in collection_ids:
        for fc in found_collections:
            if fc.id in [id, os.environ['USER'] + '_' + id]:
                matches += 1
                break

    return matches == len(collection_ids)


@given('the item {item} exists')
def step_given_stac_item_exists(context, item: str):
    context.stac_item = item
    step_given_stac_items_exist(context, item)


@then('the item {item} exists')
def step_then_stac_item_exists(context, item: str):
    step_then_stac_items_exist(context, item)


@given('the items {items} exist')
def step_given_stac_items_exist(context, items: str):
    context.stac_items = items.split(',')
    assert do_stac_items_exist(context, items.split(',')), f"No expected count of items found for {items}"


@then('the items {items} exist')
def step_then_stac_items_exist(context, items: str):
    assert do_stac_items_exist(context, items.split(',')), f"No expected count of items found for {items}"


def do_stac_items_exist(context, item_ids: list[str]) -> bool:
    # Needed until CADIP implements both POST /search AND search without collection, see RSPY-449
    found_items = create_pystac_client(context).search(
        method="GET",
        ids=item_ids,
        collections=context.stac_collections).items()
    if found_items is not None:
        logging.debug(f"Found items: {list(found_items)}")
    # found_items = create_pystac_client(context).get_items(*item_ids)
    return found_items is not None and len(list(found_items)) == len(item_ids)


@when('he checks the validity of STAC API')
def step_check_stac_api(context):
    """Validates STAC API"""
    assert context.apikey is not None, "API-KEY is not set."
    assert context.stac_api_root_url is not None, "STAC API instance has not been defined."
    assert context.stac_conformance_classes is not None, "STAC conformance classes are not set."

    (warnings, errors) = validate_api(
            root_url=context.stac_api_root_url,
            ccs_to_validate=context.stac_conformance_classes,
            collection=getattr(context, "stac_collection", None),
            geometry=getattr(context, "stac_geometry", None),
            headers={'x-api-key': context.apikey},
            auth_bearer_token=None,
            auth_query_parameter=None,
            fields_nested_property=None,
            validate_pagination=True,
            query_config=QueryConfig(
                query_comparison_field=None,
                query_eq_value=None,
                query_neq_value=None,
                query_lt_value=None,
                query_lte_value=None,
                query_gt_value=None,
                query_gte_value=None,
                query_substring_field=None,
                query_starts_with_value=None,
                query_ends_with_value=None,
                query_contains_value=None,
                query_in_field=None,
                query_in_values=None,
            ),
            transaction_collection=None,
        )
    context.stac_api_warnings = warnings
    context.stac_api_errors = errors


@then("no STAC API validation error occurs")
def step_then_no_stac_api_errors(context):
    assert context.stac_api_errors is not None, "STAC API validation has not been performed"
    assert not context.stac_api_errors, \
        f"STAC API validation errors:\n - {'\n - '.join(context.stac_api_errors)}"


@then("no STAC API validation warning occurs")
def step_then_no_stac_api_warnings(context):
    assert context.stac_api_warnings is not None, "STAC API validation has not been performed"
    assert not context.stac_api_warnings, \
        f"STAC API validation warnings:\n - {'\n - '.join(context.stac_api_warnings)}"


def create_pystac_client(context) -> Client:
    assert context.apikey is not None, "API-KEY is not set."
    assert context.stac_api_root_url is not None, "STAC API instance has not been defined."
    return Client.open(context.stac_api_root_url)


def create_rs_stac_client(context) -> RsClient:
    assert os.getenv("STAC_API_URL") is not None, "STAC_API_URL is not set."
    assert os.getenv("RSPY_HOST_CATALOG") is not None, "RSPY_HOST_CATALOG is not set."
    local_mode = "localhost" in os.getenv("STAC_API_URL")
    if local_mode:
        return RsClient(rs_server_href=None, rs_server_api_key=None).get_stac_client()
    else:
        assert context.apikey is not None, "API-KEY is not set."
        return RsClient(rs_server_href=os.getenv("STAC_API_URL"), rs_server_api_key=context.apikey).get_stac_client()


@when("he adds the collection {collection_id}")
def step_when_stac_create_collection(context, collection_id: str):
    response = create_rs_stac_client(context).add_collection(
        collection=Collection.from_file('resources/catalog/collections/' + collection_id + '.json'))
    assert (response.status_code in [201, 202, 409]), f'status for add_collection is {response.status_code}: {response.text}'


@when("he adds the item {item_id} to collection {collection_id}")
def step_when_stac_add_item(context, item_id: str, collection_id: str):
    response = create_rs_stac_client(context).add_item(
        item=Item.from_file('resources/catalog/items/' + item_id + '.json'),
        collection_id=collection_id)
    assert (response.status_code in [201, 202, 409]), f'status for add_item is {response.status_code}: {response.text}'