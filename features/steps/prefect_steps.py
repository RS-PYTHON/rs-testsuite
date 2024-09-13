from behave import given, when, then
import requests
import json
import os
from prefect import client

# Function to perform a GET request to the Prefect API
def prefect_api_get(context, endpoint: str, parameters: str) -> str:
    # Ensure the PREFECT_API_URL environment variable is set
    assert "PREFECT_API_URL" in os.environ
    # Ensure the context has cookies
    assert context.cookies is not None
    
    # Construct the URL for the GET request
    prefect_server = os.getenv("PREFECT_API_URL")       
    url = f"{os.getenv('PREFECT_API_URL')}{endpoint}/{parameters}"
    print(f"url = {url}")
        
    with requests.Session() as session:
        # Update session cookies with context cookies
        session.cookies.update(context.cookies)
        # WARNING: Need to call twice. Reason unknown.
        session.get(url)
        response = session.get(url)
        # Print the response status code and text
        print(response.status_code, flush=True)
        assert (response.status_code == 200)
        print(response.text, flush=True)        
        return response

# Function to perform a POST request to the Prefect API
def prefect_api_post(context, endpoint: str, post_data: json) -> str:
    # Ensure the PREFECT_API_URL environment variable is set
    assert "PREFECT_API_URL" in os.environ
    # Ensure the context has cookies
    assert context.cookies is not None
    
    # Construct the URL for the POST request
    prefect_server = os.getenv("PREFECT_API_URL")       
    url1 = f"{os.getenv('PREFECT_API_URL')}/api/hello"
    url = f"{os.getenv('PREFECT_API_URL')}{endpoint}/"
    print(f"url = {url}")
    print (post_data)

        
    with requests.Session() as session:
        # Update session cookies with context cookies
        session.cookies.update(context.cookies)
        # WARNING: Need to call twice. Reason unknown.
        session.get(url1)
        response = session.post(url, json.dumps(post_data))
        # Print the response status code and text
        print(response.status_code, flush=True)
        print(response.text, flush=True)        
        return response
    
    
    
""" ##########################################################################
    Step definition to check if a flow is deployed.
    Code with assertion.
    flow_id will be added to the context at the end. 
    ########################################################################## """
@given('the flow {flow} is deployed')
def step_flow_is_deployed(context: str, flow: str):
    # Perform a GET request to check the flow deployment
    response = prefect_api_get(context, '/api/flows/name', flow)    

    # Parse the response JSON and extract the flow ID
    data = json.loads(response.text)
    context.flow_id = data['id']
    # Ensure the flow ID is not None
    assert context.flow_id is not None    
    print(f"Flow id = {context.flow_id}.")


""" ##########################################################################
    Step definition to check if a flow is deployed on a specific deployment
    Code with assertion.
    flow_id and deployment_id will be added to the context at the end. 
 ########################################################################## """
@given('the flow {flow} is deployed on deployment {deployment}')
def step_flow_is_deployed(context: str, flow: str, deployment: str):
    # Perform a GET request to check the flow deployment on a specific deployment
    response = prefect_api_get(context, '/api/deployments/name', flow + '/' + deployment)      

    # Parse the response JSON and extract the deployment and flow IDs
    data = json.loads(response.text)
    context.deployment_id = data['id']
    context.flow_id = data['flow_id']
    # Ensure the deployment and flow IDs are not None
    assert context.deployment_id is not None
    assert context.flow_id is not None
        
    print(f"Flow id = {context.flow_id}.")        
    print(f"Deployment id = {context.deployment_id}.")


""" ##########################################################################
    Step definition to start the flow
    Code with assertion.
    flow_id and deployment_id will be added to the context at the end. 
 ########################################################################## """
@when('we start the flow')
def step_start_the_flow(context: str):
    # Ensure the flow ID and cookies are not None
    assert context.flow_id is not None
        
    # Define the parameters for the POST request to start the flow
    parameters_json = {
        "name": "started-cucumber",
        "flow_id": f"{context.flow_id}",
        "deployment_id":f"{context.deployment_id}"
    }
    
    # Perform a POST request to start the flow
    response = prefect_api_post(context, '/api/flow_runs', parameters_json)
    # Print the response status code and text
    exit()

""" ##########################################################################
    Step create a Flow Run From Deployment
    Code with assertion.
 ########################################################################## """
@when('we start the deployment')
def step_start_the_deployment(context: str):
    # Ensure the flow ID and cookies are not None
    assert context.deployment_id is not None
        
    # Define the parameters for the POST request to start the flow
    parameters_json = {
        "name": "started-cucumber2",
    }
    
    # Perform a POST request to start the flow
    response = prefect_api_post(context, f'/api/deployments/{context.deployment_id}/create_flow_run', parameters_json)
    
    # Print the response status code and text
    exit()


""" ##########################################################################
    Step resume the deployment
    Code with assertion.
 ########################################################################## """
@when('we resume the deployment')
def step_resume_the_deployment(context: str):
    # Ensure the flow ID and cookies are not None
    assert context.deployment_id is not None
        
    # Define the parameters for the POST request to start the flow
    parameters_json = {}
    
    # Perform a POST request to start the flow
    response = prefect_api_post(context, f'/api/deployments/{context.deployment_id}/resume_deployment', parameters_json)
    
    # Print the response status code and text
    exit()


#  https://processing.ops.rs-python.eu/api/deployment/fa709911-868b-41cc-8d04-63ca61605b4e/create_flow_run/
