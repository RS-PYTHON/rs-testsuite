from behave import given, when, then
from rs_server import rs_server_get, rs_server_post , rs_server_delete


"""
Check the staging url
"""
@then ('the staging URL exists')
def step_check_stagin(context):
    rs_server_get(context, 'processes', 200)
    rs_server_get(context, 'processes/staging', 200)
    process_json = {}
    rs_server_post(context, 'processes/staging/execution', process_json, 200)
    rs_server_get(context, 'jobs', 200)
    rs_server_get(context, 'jobs/12345678', 404)
    rs_server_delete(context, 'jobs/12345678', 200)    
    rs_server_get(context, 'jobs/12345678/results', 200)
    
    
    