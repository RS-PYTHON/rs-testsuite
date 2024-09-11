from behave import given, when, then
import requests
import json
import requests



@when ('we deploy a flow')
def step_deploy_a_flow(context: str):
    """
    Check Github entry
    """
    with requests.Session() as session:
        session.cookies.update(context.cookies)

        prefect_server_url = "https://processing.ops.rs-python.eu"
        
        flow_json = {
            "project_id": "PROJETA",
            "url": "https://github.com/RS-PYTHON/rs-testsuite/blob/feature/endpoint/flows/hello_world.py"
        }
        
        #response = session.get(f"{prefect_server_url}/api/health/")
        response = session.post(f"{prefect_server_url}/api/flows/", data=json.dumps(flow_json))
        response.raise_for_status()
        print(response.status_code, flush=True)
        print (response.text, flush=True)

        assert (True)
 
 

 
"""
 def step_deploy_a_flow(context: str):
    with requests.Session() as session:
        session.cookies.update(context.cookies)

        prefect_server_url = "https://processing.ops.rs-python.eu"
        
        flow_json = {
            "name": "concombre",
            "flow_id": "68af8f2b-6d16-4d3b-9f0f-73678520ec05",
            "work_pool_name" : "on-demand-k8s-pool"
        }
        
        #response = session.get(f"{prefect_server_url}/api/health/")
        response = session.post(f"{prefect_server_url}/api/deployments/", data=json.dumps(flow_json))
        response = session.post(f"{prefect_server_url}/api/deployments/", data=json.dumps(flow_json))
        response.raise_for_status()
        print(response.status_code, flush=True)
        print (response.text, flush=True)

        assert (True)
 
 """