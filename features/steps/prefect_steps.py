from behave import given, when, then
import requests
import json
import requests
import os
from prefect import client

# GET command
def get_request(context, endpoint : str, parameters : str) -> str:
    assert "PREFECT_API_URL" in os.environ
    assert context.cookies is not None
    
    prefect_server= os.getenv("PREFECT_API_URL")       
    url = f"{os.getenv("PREFECT_API_URL")}{endpoint}/{parameters}"
    print (f"url = {url}")
        
    with requests.Session() as session:
        session.cookies.update(context.cookies)
        # WARNING : need to call twice. We do not know why yet !!!
        session.get(url)
        response=session.get(url)
        print(response.status_code, flush=True)
        print(response.text, flush=True)        
        return response


@given('the flow {flow} is deployed')
def step_flow_is_deployed(context: str, flow: str):
    response = get_request(context, '/api/flows/name', flow)    
    data = json.loads (response.text )
    context.flow_id = data['id']
    assert context.flow_id is not None    
    print(f"Flow id = {context.flow_id}.")
        

@given('the flow {flow} is deployed on deployment {deployment}')
def step_flow_is_deployed(context: str, flow: str, deployment: str):
    response = get_request(context, '/api/deployments/name', flow + '/' + deployment)      

    data = json.loads (response.text )
    context.deployment_id = data['id']
    context.flow_id = data['flow_id']
    assert context.deployment_id is not None
    assert context.flow_id is not None
        
    print(f"Flow id = {context.flow_id}.")        
    print(f"Deployment id = {context.deployment_id}.")        
        

@when('we start the flow')
def step_start_the_flow(context: str):
    assert context.flow_id is not None
    assert context.cookies is not None
    assert context.prefect_server is not None
    
    with requests.Session() as session:
        session.cookies.update(context.cookies)
        
        parameters_json = {
            "name" : "started-cucumber",
            "flow_id": f"{context.flow_id}"
        }
    
        
        chain = f"{context.prefect_server}/api/flow_runs/"
        print (chain, flush=True)
        print (parameters_json, flush=True)
        
        response = session.post(chain, data=json.dumps(parameters_json)) 
        response = session.post(chain, data=json.dumps(parameters_json)) 
        response.raise_for_status()
        print(response.status_code, flush=True)
        print (response.text, flush=True)
        exit() 
    


    
"""
        parameters_json = {
            "name": f"{flow}"
        }
        print (parameters_json, flush=True)
        #response = session.post(chain, data=json.dumps(parameters_json))     

"""        




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



 """