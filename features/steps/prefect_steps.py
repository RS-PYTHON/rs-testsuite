from behave import given, when, then
import requests
import json
import requests
import os
from prefect import client

# GET command
def prefect_api_get(context, endpoint : str, parameters : str) -> str:
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

# POST command
def prefect_api_post(context, endpoint : str, post_data : json) -> str:
    assert "PREFECT_API_URL" in os.environ
    assert context.cookies is not None
    
    prefect_server= os.getenv("PREFECT_API_URL")       
    url = f"{os.getenv("PREFECT_API_URL")}{endpoint}"
    print (f"url = {url}")
        
    with requests.Session() as session:
        session.cookies.update(context.cookies)
        # WARNING : need to call twice. We do not know why yet !!!
        session.post(url, json.dumps(post_data))
        response=session.post(url, json.dumps(post_data))
        print(response.status_code, flush=True)
        print(response.text, flush=True)        
        return response


@given('the flow {flow} is deployed')
def step_flow_is_deployed(context: str, flow: str):
    response = prefect_api_get(context, '/api/flows/name', flow)    

    data = json.loads (response.text )
    context.flow_id = data['id']
    assert context.flow_id is not None    
    print(f"Flow id = {context.flow_id}.")
        

@given('the flow {flow} is deployed on deployment {deployment}')
def step_flow_is_deployed(context: str, flow: str, deployment: str):
    response = prefect_api_get(context, '/api/deployments/name', flow + '/' + deployment)      

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
        
    parameters_json = {
            "name" : "started-cucumber",
            "flow_id": f"{context.flow_id}"
    }
    
    response = prefect_api_post('/api/flow_runs', parameters_json)
    print(response.status_code, flush=True)
    print (response.text, flush=True)
    exit() 
    


