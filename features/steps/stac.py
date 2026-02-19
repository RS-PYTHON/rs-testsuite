import cProfile
import json
import logging
import os
import pstats
from collections.abc import Iterator
from pathlib import Path

import pyprof2calltree
from behave import given, then, use_step_matcher, when
from pystac import Collection, Item
from pystac_client import Client
from pystac_client.exceptions import APIError
from rs_client.rs_client import RsClient
from rs_client.stac.auxip_client import AuxipClient
from rs_client.stac.cadip_client import CadipClient
from rs_client.stac.catalog_client import CatalogClient

# from rs_client.stac.edrs_client import EdrsClient
# from rs_client.stac.lta_client import LtaClient
from rs_client.stac.prip_client import PripClient
from rs_client.stac.stac_base import StacBase
from stac_api_validator.validations import QueryConfig, validate_api

logger = logging.getLogger(__name__)


use_step_matcher("re")


@given("the (?P<stac_instance>CATALOG|CADIP|AUXIP|LTA|PRIP) STAC API")
def step_given_stac_api(context, stac_instance: str):
    for url in [
        "CATALOG_STAC_API_URL",
        "CADIP_STAC_API_URL",
        "AUXIP_STAC_API_URL",
        "LTA_STAC_API_URL",
        "PRIP_STAC_API_URL",
        "EDRS_STAC_API_URL",
    ]:
        assert os.getenv(url) is not None, url + " is not set."
    context.stac_api_root_url = os.environ[
        {
            "CATALOG": "CATALOG_STAC_API_URL",
            "CADIP": "CADIP_STAC_API_URL",
            "AUXIP": "AUXIP_STAC_API_URL",
            "LTA": "LTA_STAC_API_URL",
            "PRIP": "PRIP_STAC_API_URL",
            "EDRS": "EDRS_STAC_API_URL",
        }[stac_instance]
    ]
    context.rs_stac_client = {
        "CATALOG": create_rs_stac_client_catalog,
        "CADIP": create_rs_stac_client_cadip,
        "AUXIP": create_rs_stac_client_auxip,
        #        "LTA": create_rs_stac_client_lta,
        "PRIP": create_rs_stac_client_prip,
        #        "EDRS": create_rs_stac_client_edrs,
    }[stac_instance](context)
    context.stac_instance = stac_instance


use_step_matcher("parse")


@given("a set of STAC conformance classes")
def step_given_stac_conformance_classes(context):
    context.stac_conformance_classes = []
    for row in context.table:
        context.stac_conformance_classes.append(row["class"])


@given("the bbox {bbox}")
def step_given_stac_bbox(context, bbox: str):
    bb = json.loads(bbox)
    context.stac_geometry = json.dumps(
        {
            "type": "Polygon",
            "coordinates": [
                [[bb[0], bb[1]], [bb[0], bb[3]], [bb[2], bb[3]], [bb[2], bb[1]]],
            ],
        },
    )


@given('the collection "{collection}" exists')
def step_given_stac_collection_exists(context, collection: str):
    context.stac_collection = collection
    step_given_stac_collections_exist(context, [collection])


@then('the collection "{collection}" exists')
def step_then_stac_collection_exists(context, collection: str):
    step_then_stac_collections_exist(context, [collection])


@given('the collections "{collections:StrList}" exist')
def step_given_stac_collections_exist(context, collections: list[str]):
    context.stac_collections = collections
    assert_stac_collections_exist(context, collections)


@then('the collections "{collections:StrList}" exist')
def step_then_stac_collections_exist(context, collections: list[str]):
    assert_stac_collections_exist(context, collections)


def assert_stac_collections_exist(context, collections: list[str]):
    assert do_stac_collections_exist(
        context,
        collections,
    ), f"No expected count of collections found for {collections}"


@given('the collection "{collection}" does not exist')
def step_given_stac_collection_does_not_exist(context, collection: str):
    context.stac_collection = collection
    step_given_stac_collections_do_not_exist(context, [collection])


@given('the collections "{collections:StrList}" do not exist')
def step_given_stac_collections_do_not_exist(context, collections: list[str]):
    context.stac_collections = collections
    assert not do_stac_collections_exist(
        context,
        collections,
    ), f"No expected count of collections found for {collections}"


def do_stac_collections_exist(context, collection_ids: list[str]) -> bool:
    context.stac_collections = []
    for collection_id in collection_ids:
        context.stac_collections.append(collection_id)
        # Explicit prefixing needed for some tests because search by implicit naming does not work
    #        if (os.environ['USER'] not in collection_id):
    #            context.stac_collections.append(os.environ['USER'] + '_' + collection_id)

    found_collections = create_pystac_client(context).get_collections()
    assert found_collections is not None, f"No collections found for {collection_ids}"
    matches = 0
    for cid in collection_ids:
        for fc in found_collections:
            if fc.id in [
                cid,
                os.environ["USER"] + "_" + cid,
                context.login + "_" + cid,
            ]:
                matches += 1
                break

    return matches == len(collection_ids)


@given("the item {item} exists")
def step_given_stac_item_exists(context, item: str):
    context.stac_item = item
    step_given_stac_items_exist(context, [item])


@then("the item {item} exists")
def step_then_stac_item_exists(context, item: str):
    step_then_stac_items_exist(context, [item])


@given("the items {items:StrList} exist")
def step_given_stac_items_exist(context, items: list[str]):
    context.stac_items = items
    assert do_stac_items_exist(
        context,
        items,
    ), f"No expected count of items found for {items}"


@then("the items {items:StrList} exist")
def step_then_stac_items_exist(context, items: list[str]):
    assert do_stac_items_exist(
        context,
        items,
    ), f"No expected count of items found for {items}"


def do_stac_items_exist(context, item_ids: list[str]) -> bool:
    # Needed until CADIP implements both POST /search AND search without collection, see RSPY-449
    found_items = list(
        create_pystac_client(context)
        .search(method="GET", ids=item_ids, collections=context.stac_collections)
        .items()
        or [],
    )
    logging.debug(
        "Found %d items for %d expected: %s",
        len(found_items),
        len(item_ids),
        str(found_items),
    )
    # found_items = create_pystac_client(context).get_items(*item_ids)
    return found_items is not None and len(found_items) == len(item_ids)


@when("he checks the validity of STAC API")
def step_check_stac_api(context):
    """Validates STAC API"""
    assert context.apikey is not None, "API-KEY is not set."
    assert (
        context.stac_api_root_url is not None
    ), "STAC API instance has not been defined."
    assert (
        context.stac_conformance_classes is not None
    ), "STAC conformance classes are not set."
    assert isinstance(context.stac_instance, str), "STAC instance type is not set."

    profiler = cProfile.Profile()
    profiler.enable()

    (warnings, errors) = validate_api(
        root_url=context.stac_api_root_url,
        ccs_to_validate=context.stac_conformance_classes,
        collection=getattr(context, "stac_collection", None),
        geometry=getattr(context, "stac_geometry", None),
        headers={"x-api-key": context.apikey},
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
        open_assets_urls=False,
        stac_check_config=f"./stac-check-config-{context.stac_instance.lower()}.yaml",
    )
    context.stac_api_warnings = warnings
    context.stac_api_errors = errors

    profiler.disable()
    stats = pstats.Stats(profiler)
    conv = pyprof2calltree.CalltreeConverter(stats)
    with open("callgrind-step_check_stac_api.out", "w", encoding="utf-8") as fd:
        conv.output(fd)


@when(
    'he searches the {which_item} item of type "{product_type}" for platform "{platform}" in collection "{collection}"',
)
def step_search_stac_item(
    context,
    which_item: str,
    product_type: str,
    platform: str,
    collection: str,
):
    assert (
        context.rs_stac_client is not None
    ), "STAC API client has not been initialized"
    stac_client: StacBase = context.rs_stac_client
    context.stac_item = stac_client.search(
        method="POST",
        max_items=1,
        limit=1,
        collections=collection,
        stac_filter={
            "op": "and",
            "args": [
                {"op": "=", "args": [{"property": "product:type"}, product_type]},
                {"op": "=", "args": [{"property": "platform"}, platform]},
            ],
        },
        sortby=[
            {
                "field": "start_datetime",
                "direction": "asc" if which_item == "oldest" else "desc",
            },
        ],
    )[0]


@when("he retrieves all collections")
def step_retrieve_all_collections(context):
    assert (
        context.rs_stac_client is not None
    ), "STAC API client has not been initialized"
    stac_client: StacBase = context.rs_stac_client
    context.stac_all_collections = stac_client.get_collections()


@then("each collection has at least {num_items:d} item")
@then("each collection has at least {num_items:d} items")
def step_each_collection_contains_at_least_num_items(context, num_items: int):
    assert (
        context.stac_all_collections is not None
    ), "STAC API client returned no collections"
    all_collections: Iterator[Collection] = context.stac_all_collections
    results = {}
    for collection in all_collections:
        all_items: Iterator[Item] = collection.get_items()
        count = 0
        for _ in range(num_items):
            try:
                next(all_items)
                count += 1
            except (APIError, StopIteration):
                break

        has_enough = count >= num_items
        results[collection.id] = has_enough

    report_path = Path(context.stac_instance + "_stac_collection_report.json")
    with report_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # CADIP: No Sentinel-1 products found at Punta Arenas, but it seems normal
    # PRIP: S1 EN/NM/Z* produced only during commissioning phase + very rare calibration campaigns
    # PRIP: S2 MSI_L1A are produced quite rarely - https://esa-cams.atlassian.net/browse/GSANOM-20505
    # PRIP: S3 OL_0_CR1__* produced only during commissioning phase
    # PRIP: S3 OL_1_SPC___ produced only every three months
    ignored_cid = [
        "S1_PAR",
        "S1A_L0_EN_S",
        "S1A_L0_NM_S",
        "S1A_L0_ZM_S",
        "S1A_L0_ZE_S",
        "S1A_L0_ZI_S",
        "S1A_L0_ZW_S",
        "S1C_L0_EN_S",
        "S1C_L0_NM_S",
        "S1C_L0_ZM_S",
        "S1C_L0_ZE_S",
        "S1C_L0_ZI_S",
        "S1C_L0_ZW_S",
        "S1D_L0_EN_S",
        "S1D_L0_NM_S",
        "S1D_L0_ZM_S",
        "S1D_L0_ZE_S",
        "S1D_L0_ZI_S",
        "S1D_L0_ZW_S",
        "S2A_L1_MSI_L1A",
        "S2B_L1_MSI_L1A",
        "S2C_L1_MSI_L1A",
        "S3A_L0_OL_0_CR1",
        "S3B_L0_OL_0_CR1",
        "S3A_L1_OL_SPC",
        "S3B_L1_OL_SPC",
    ]
    missing = [
        cid for cid, ok in results.items() if not ok and cid.upper() not in ignored_cid
    ]
    assert not missing, f"Some collections have fewer than {num_items} items: {missing}"


@then("no STAC API validation error occurs")
def step_then_no_stac_api_errors(context):
    assert (
        context.stac_api_errors is not None
    ), "STAC API validation has not been performed"
    stac_api_errors: list[str] = list(context.stac_api_errors)
    if context.stac_api_root_url in [
        os.environ["CATALOG_STAC_API_URL"],
        os.environ["CADIP_STAC_API_URL"],
        os.environ["AUXIP_STAC_API_URL"],
        os.environ["EDRS_STAC_API_URL"],
    ]:
        # Ignore bbox errors for CADIP/AUXIP as we have items without geometry
        for ignored_geometry_error in [
            "[Item Search] GET Search with ids and non-intersecting bbox returned results, "
            "indicating the ids parameter is overriding the bbox parameter. "
            "All parameters are applied equally since STAC API 1.0.0-beta.1",
            "[Item Search] POST Search with ids and non-intersecting bbox returned results, "
            "indicating the ids parameter is overriding the bbox parameter. "
            "All parameters are applied equally since STAC API 1.0.0-beta.1",
        ]:
            if ignored_geometry_error in stac_api_errors:
                stac_api_errors.remove(ignored_geometry_error)
    if context.stac_api_root_url == os.environ["CATALOG_STAC_API_URL"]:
        # Ignore known Catalog errors traced by an anomaly
        for ignored_catalog_error in [
            "[Collections] /collections self link does not match requested url",  # RSPY-950
        ]:
            if ignored_catalog_error in stac_api_errors:
                stac_api_errors.remove(ignored_catalog_error)
    assert (
        not stac_api_errors
    ), f"STAC API validation errors:\n - {'\n - '.join(stac_api_errors)}"


@then("no STAC API validation warning occurs")
def step_then_no_stac_api_warnings(context):
    assert (
        context.stac_api_warnings is not None
    ), "STAC API validation has not been performed"
    # Ignore warnings for stories not yet implemented
    stac_api_warnings = [
        warning
        for warning in context.stac_api_warnings
        if "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" not in warning
    ]
    assert (
        not stac_api_warnings
    ), f"STAC API validation warnings:\n - {'\n - '.join(stac_api_warnings)}"


@then('the item "{item_id}" is returned')
def step_then_item_returned(context, item_id: str):
    assert context.stac_item is not None, "STAC Item Search has not been performed"
    assert (
        item_id == context.stac_item.id
    ), f"Retrieved: {context.stac_item.id}\n^^^^^^^^^^^^^^^^  Expected : {item_id}"


def create_pystac_client(context) -> Client:
    assert context.apikey is not None, "API-KEY is not set."
    assert (
        context.stac_api_root_url is not None
    ), "STAC API instance has not been defined."
    return Client.open(context.stac_api_root_url, {"x-api-key": context.apikey})


def create_rs_stac_client_auxip(context) -> AuxipClient:
    return create_rs_stac_client(context, "auxip")


def create_rs_stac_client_cadip(context) -> CadipClient:
    return create_rs_stac_client(context, "cadip")


def create_rs_stac_client_catalog(context) -> CatalogClient:
    return create_rs_stac_client(context, "catalog")


# def create_rs_stac_client_edrs(context) -> EdrsClient:
#    return create_rs_stac_client(context, "edrs")


# def create_rs_stac_client_lta(context) -> LtaClient:
#    return create_rs_stac_client(context, "lta")


def create_rs_stac_client_prip(context) -> PripClient:
    return create_rs_stac_client(context, "prip")


def create_rs_stac_client(context, instance: str) -> RsClient:
    env_var = f"{instance.upper()}_STAC_API_URL"
    stac_api_url = os.getenv(env_var)
    assert stac_api_url is not None, f"{env_var} is not set."

    local_mode = "localhost" in stac_api_url
    if local_mode:
        client = RsClient(rs_server_href=None, rs_server_api_key=None)
    else:
        rspy_host = os.getenv("RSPY_HOST_CATALOG")
        assert rspy_host is not None, "RSPY_HOST_CATALOG is not set."
        assert context.apikey is not None, "API-KEY is not set."
        client = RsClient(
            rs_server_href=rspy_host,
            rs_server_api_key=context.apikey,
            owner_id=context.login,
        )

    return getattr(client, f"get_{instance.lower()}_client")(timeout=10)


@when("he adds the collection {collection_id}")
def step_when_stac_create_collection(context, collection_id: str):
    response = create_rs_stac_client_catalog(context).add_collection(
        collection=Collection.from_file(
            "resources/catalog/collections/" + collection_id + ".json",
        ),
        raise_for_status=False,
    )
    assert response.status_code in [
        201,
        202,
        409,
    ], f"status for add_collection is {response.status_code}: {response.text}"


@when("he adds the item {item_id} to collection {collection_id}")
def step_when_stac_add_item(context, item_id: str, collection_id: str):
    response = create_rs_stac_client_catalog(context).add_item(
        item=Item.from_file("resources/catalog/items/" + item_id + ".json"),
        collection_id=collection_id,
        raise_for_status=False,
    )
    assert response.status_code in [
        201,
        202,
        409,
    ], f"status for add_item is {response.status_code}: {response.text}"
