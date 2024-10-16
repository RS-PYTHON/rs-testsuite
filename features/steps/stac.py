from behave import given, when, then
from behave import use_step_matcher
from pystac import Collection, Item
from rs_client.rs_client import RsClient
from stac_api_validator.validations import QueryConfig
from stac_api_validator.validations import validate_api

import os


@given('a set of STAC conformance classes')
def step_given_stac_conformance_classes(context):
    context.stac_conformance_classes = []
    for row in context.table:
        context.stac_conformance_classes.append(row['class'])


@given('the bbox {bbox}')
def step_given_stac_bbox(context, bbox: list[float]):
    context.stac_geometry = bbox


@given('the collection {collection}')
def step_given_stac_collection(context, collection: str):
    context.stac_collection = collection


use_step_matcher("re")


@when('he checks the validity of (?P<stac_instance>CATALOG|CADIP|AUXIP|LTA|PRIP) STAC API')
def step_check_stac_api(context, stac_instance: str):
    """Validates STAC API"""
    assert context.apikey is not None, "API-KEY is not set."
    assert context.stac_conformance_classes is not None, "STAC conformance classes are not set."
    for url in ['STAC_API_URL', 'CADIP_STAC_API_URL', 'AUXIP_STAC_API_URL', 'LTA_STAC_API_URL', 'PRIP_STAC_API_URL']:
        assert os.getenv(url) is not None, url + " is not set."

    (warnings, errors) = validate_api(
            root_url=os.environ[{
                'CATALOG': 'STAC_API_URL',
                'CADIP': 'CADIP_STAC_API_URL',
                'AUXIP': 'AUXIP_STAC_API_URL',
                'LTA': 'LTA_STAC_API_URL',
                'PRIP': 'PRIP_STAC_API_URL'
                }[stac_instance]],
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


use_step_matcher("parse")


@then("no STAC API validation error occurs")
def step_then_no_stac_api_errors(context):
    assert context.stac_api_errors is not None, "STAC API validation has not been performed"
    assert len(context.stac_api_errors.as_list()) == 0, f"STAC API validation errors: {context.stac_api_errors}"


@then("no STAC API validation warning occurs")
def step_then_no_stac_api_warnings(context):
    assert context.stac_api_warnings is not None, "STAC API validation has not been performed"
    assert len(context.stac_api_warnings.as_list()) == 0, f"STAC API validation errors: {context.stac_api_warnings}"


def create_stac_client(context):
    assert os.getenv("STAC_API_URL") is not None, "STAC_API_URL is not set."
    assert os.getenv("RSPY_HOST_CATALOG") is not None, "RSPY_HOST_CATALOG is not set."
    local_mode = "localhost" in os.getenv("STAC_API_URL")
    if local_mode:
        return RsClient(rs_server_href=None, rs_server_api_key=None).get_stac_client()
    else:
        assert context.apikey is not None, "API-KEY is not set."
        return RsClient(rs_server_href=os.getenv("STAC_API_URL"), rs_server_api_key=context.apikey).get_stac_client()


@when("he adds a collection from {json_file}")
def step_when_stac_create_collection(context, json_file: str):
    response = create_stac_client(context).add_collection(collection=Collection.from_file(json_file))
    assert (response.status_code in [201, 202, 409]), f'status for add_collection is {response.status_code}: {response.text}'


@when("he adds an item to collection {collection} from {json_file}")
def step_when_stac_add_item(context, collection: str, json_file: str):
    response = create_stac_client(context).add_item(item=Item.from_file(json_file), collection_id=collection)
    assert (response.status_code in [201, 202, 409]), f'status for add_item is {response.status_code}: {response.text}'
