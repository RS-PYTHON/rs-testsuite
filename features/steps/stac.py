from behave import given, when, then
from behave import use_step_matcher
from stac_api_validator.validations import QueryConfig
from stac_api_validator.validations import validate_api

import os


@given('a set of STAC conformance classes')
def step_given_stac_conformance_classes(context):
    context.stac_conformance_classes = []
    for row in context.table:
        context.stac_conformance_classes.append(row['class'])


use_step_matcher("re")


@when('he checks the validity of (?P<stac_instance>CATALOG|CADIP|AUXIP|LTA|PRIP) STAC API')
def step_check_stac_api(context, stac_instance: str):
    """Validates STAC API"""
    assert context.apikey is not None, "API-KEY is not set."
    assert context.stac_conformance_classes is not None, "STAC conformance classes are not set."
    assert os.getenv("STAC_API_URL") is not None, "STAC_API_URL is not set."

    (warnings, errors) = validate_api(
            root_url=os.getenv({
                'CATALOG': 'STAC_API_URL',
                'CADIP': 'CADIP_STAC_API_URL',
                'AUXIP': 'AUXIP_STAC_API_URL',
                'LTA': 'LTA_STAC_API_URL',
                'PRIP': 'PRIP_STAC_API_URL'
                }[stac_instance]),
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
    assert len(context.stac_api_errors.as_list()) == 0, f"STAC API validation errors: {context.stac_api_errors}"


@then("no STAC API validation warning occurs")
def step_then_no_stac_api_warnings(context):
    assert context.stac_api_warnings is not None, "STAC API validation has not been performed"
    assert len(context.stac_api_warnings.as_list()) == 0, f"STAC API validation errors: {context.stac_api_warnings}"
