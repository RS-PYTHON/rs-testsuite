from behave import then
from rs_server import rs_server_post


@then("staging post url succeeds")
def step_check_staging(context):
    """
    Check the staging url
    """
    process_json = {
        "inputs": {
            "collection": "s03-aux-osf",
            "items": {
                "href": "https://auxip.copernicus.eu/odata/v1/Products%28dacd3964-f366-11ef-b549-0050561a7772%29/$value",
            },
        },
    }
    rs_server_post(context, "processes/staging", process_json, 200)
