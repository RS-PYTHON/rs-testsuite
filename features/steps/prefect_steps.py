from behave import given, when, then

import requests
import json
import os, sys



# Function to perform a GET request to the Prefect API
def prefect_api_get(context, endpoint: str, parameters: str) -> str:
    # Ensure the PREFECT_API_URL environment variable is set
    assert "PREFECT_API_URL" in os.environ
    # Ensure the context has cookies
    assert context.cookies is not None
    
    # Construct the URL for the GET request
    url = f"{os.getenv('PREFECT_API_URL')}{endpoint}/{parameters}"
    print(f"url = {url}")
        
    with requests.Session() as session:
        # Update session cookies with context cookies
        session.cookies.update(context.cookies)
        # Call HTTP GET method
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
    url = f"{os.getenv('PREFECT_API_URL')}{endpoint}/"
    print(f"url = {url}")
    print (post_data)

        
    with requests.Session() as session:
        # Update session cookies with context cookies
        session.cookies.update(context.cookies)
        # Call the HTTP.POST method
        response = session.post(url, json.dumps(post_data))
        # Print the response status code and text
        print(response.status_code, flush=True)
        #print(response.text, flush=True)        
        return response
    
    
    
"""
Step definition to check if a flow is deployed.

Args:
    context: The context object provided by Behave.
    flow (str): The name of the flow to check.

Asserts:
    The flow ID is not None.
"""
@given('the flow {flow} is deployed')
def step_flow_is_deployed(context, flow: str):
    # Perform a GET request to check the flow deployment
    response = prefect_api_get(context, '/api/flows/name', flow)    

    # Parse the response JSON and extract the flow ID
    data = json.loads(response.text)
    context.flow_id = data['id']
    # Ensure the flow ID is not None
    assert context.flow_id is not None    
    print(f"Flow id = {context.flow_id}.")


"""
Step definition to check if a flow is deployed on a specific deployment.

Args:
    context: The context object provided by Behave.
    flow (str): The name of the flow to check.
    deployment (str): The name of the deployment to check.

Asserts:
    The deployment ID and flow ID are not None.
"""
@given('the flow {flow} is deployed on deployment {deployment}')
def step_flow_is_deployed(context, flow: str, deployment: str):
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


"""
Step definition to start the flow.

Args:
    context: The context object provided by Behave.

Asserts:
    The flow ID and deployment ID are not None.
    The response status code is between 200 and 299.
"""
@when('we start the flow')
def step_start_the_flow(context):
    # Ensure the flow ID and cookies are not None
    assert context.flow_id is not None
    assert context.deployment_id is not None

    # Define the parameters for the POST request to start the flow
    parameters_json = {
        "name" : "flow-run-from-cucumber",
         "tags": [
            "CUCUMBER",
            "TEST"
                ],
        }
    
    # Perform a POST request to start the flow
    response = prefect_api_post(context, f'/api/deployments/{context.deployment_id}/create_flow_run', parameters_json)
    data = json.loads(response.text)
    context.flow_run_id = data['id']
    assert context.flow_run_id is not None 
    assert (response.status_code >= 200) and (response.status_code < 300)


@then('the flow ends without error')
def step_check_flow_artefacts(context):
    # Ensure the flow ID and cookies are not None
    assert context.flow_run_id is not None

    # Define the parameters for the POST request to start the flow
    parameters_json = {
        "artifacts": {
            "flow_run_id": {
            "any_": [f"{context.flow_run_id}"]
        }}}
    
    
    
    #{"flow_run_id":  [f"{context.flow_run_id}"]}
    
    
    # Perform a POST request to start the flow
    response = prefect_api_post(context, f'/api/artifacts/latest/filter', parameters_json)
    assert (response.status_code >= 200) and (response.status_code < 300)
    data = json.loads(response.text)
    print (data)
    
    steps = json.loads(data[0]['data'])

    # Vérifier si tous les steps sont "OK"
    all_ok = all(step['status'] == 'OK' for step in steps)
    assert (all_ok)


