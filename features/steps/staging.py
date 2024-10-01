from behave import then
from rs_server import rs_server_post


@then('staging post url succeeds')
def step_check_staging(context):
    """
    Check the staging url
    """
    process_json = {}
    rs_server_post(context, 'processes/staging/execution', process_json, 200)
