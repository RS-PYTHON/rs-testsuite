from behave import given, when, then
from rs_server import rs_server_get, rs_server_post , rs_server_delete


"""
Check the staging url
"""
@then ('staging post url succeeds')
def step_check_staging(context):
    process_json = {}
    
    
    