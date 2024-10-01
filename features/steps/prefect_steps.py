from behave import given, when, then

import requests
import json
import os
import time


# Function to perform a GET request to the Prefect API
def prefect_api_get(context, endpoint: str, parameters: str) -> str:
    # Ensure the PREFECT_API_URL environment variable is set
    assert "PREFECT_API_URL" in os.environ, "PREFECT_API_URL environment variable is not set."
    # Ensure the context has cookies
    assert context.cookies is not None, "Cookies are missing on the execution context."

    # Construct the URL for the GET request
    url = f"{os.getenv('PREFECT_API_URL')}{endpoint}/{parameters}"

    with requests.Session() as session:
        # Update session cookies with context cookies
        session.cookies.update(context.cookies)
        # Call HTTP GET method
        response = session.get(url)
        # Print the response status code and text
        print(response.status_code, flush=True)

        assert (response.status_code == 200), f'status for GET {url} is {response.status_code} and not 200.'

        print(response.text, flush=True)
        return response


# Function to perform a POST request to the Prefect API
def prefect_api_post(context, endpoint: str, post_data: json) -> str:
    # Ensure the PREFECT_API_URL environment variable is set
    assert "PREFECT_API_URL" in os.environ, "PREFECT_API_URL environment variable is not set."
    # Ensure the context has cookies
    assert context.cookies is not None, "Cookies are missing on the execution context."

    # Construct the URL for the POST request
    url = f"{os.getenv('PREFECT_API_URL')}{endpoint}/"
    print(f"url = {url}")
    print(post_data)

    with requests.Session() as session:
        # Update session cookies with context cookies
        session.cookies.update(context.cookies)
        # Call the HTTP.POST method
        response = session.post(url, json.dumps(post_data))
        # Print the response status code and text
        print(response.status_code, flush=True)
        return response


@given('the flow {flow} is deployed')
def step_flow_is_deployed(context, flow: str):
    """
    Step definition to check if a flow is deployed.

    Args:
        context: The context object provided by Behave.
        flow (str): The name of the flow to check.

    Asserts:
        The flow ID is not None.
    """
    # Perform a GET request to check the flow deployment
    response = prefect_api_get(context, '/api/flows/name', flow)

    # Parse the response JSON and extract the flow ID
    data = json.loads(response.text)
    context.flow_id = data['id']
    # Ensure the flow ID is not None
    assert context.flow_id is not None, "Flow id could not be extracted from data."
    print(f"Flow id = {context.flow_id}.")


@given('the flow {flow} is deployed on deployment {deployment}')
def step_flow_is_deployed_on_deployment(context, flow: str, deployment: str):
    """
    Step definition to check if a flow is deployed on a specific deployment.

    Args:
        context: The context object provided by Behave.
        flow (str): The name of the flow to check.
        deployment (str): The name of the deployment to check.

    Asserts:
        The deployment ID and flow ID are not None.
    """
    # Perform a GET request to check the flow deployment on a specific deployment
    response = prefect_api_get(context, '/api/deployments/name', flow + '/' + deployment)      
    assert response.status_code == 200, f'GET request ends with status {response.status_code}. Not a 200 answer.'


    # Parse the response JSON and extract the deployment and flow IDs
    data = json.loads(response.text)
    context.deployment_id = data['id']
    context.flow_id = data['flow_id']
    # Ensure the deployment and flow IDs are not None
    assert context.deployment_id is not None, "Deployment id is not set on the context environment."
    assert context.flow_id is not None, "Flow id is not set on the context environment."

    print(f"Flow id = {context.flow_id}.")
    print(f"Deployment id = {context.deployment_id}.")


@when('we start the flow')
def step_start_the_flow(context):
    """
    Step definition to start the flow.

    Args:
    context: The context object provided by Behave.

    Asserts:
    The flow ID and deployment ID are not None.
    The response status code is between 200 and 299.
    """
    # Ensure the flow ID and cookies are not None
    assert context.flow_id is not None, "Flow id is not set on the context environment."
    assert context.deployment_id is not None,  "Deployment id is not set on the context environment."

    # Define the parameters for the POST request to start the flow
    parameters_json = {
        "name": "flow-run-from-cucumber",
        "tags": [
            "CUCUMBER",
            "TEST"
                ],
        }

    # Perform a POST request to start the flow
    response = prefect_api_post(context, f'/api/deployments/{context.deployment_id}/create_flow_run', parameters_json)
    data = json.loads(response.text)
    print(data)
    context.flow_run_id = data['id']
    assert context.flow_run_id is not None, f"Flow run identifier could not be extraced from data['id'] :\n {data}."
    assert (response.status_code >= 200) and (response.status_code < 300), \
        f'POST request ends with status {response.status_code}. Not a 2XX answer.'


@then('the flow ends with status completed')
def step_wait_the_flow_to_complete(context):
    assert context.flow_run_id is not None, "Flow run id is not set on the context environment."

    status = "UNKNOWN"

    while (status not in ['COMPLETED', 'FAILED', 'CANCELLED', 'CRASHED', 'CANCELLING']):
        # Effectue!= 'COMPLETED'):
        time.sleep(1)

        response = prefect_api_get(context, '/api/flow_runs', context.flow_run_id)
        data = json.loads(response.text)
        flow_state_id = data['state_id']

        response = prefect_api_get(context, '/api/flow_run_states', flow_state_id)
        # Parse the response JSON and extract the deployment and flow IDs
        data = json.loads(response.text)
        status = data['type']

    assert (status == 'COMPLETED'), f"Flow ends with status {status} instead of 'Completed'."

    # Get test results
    parameters_json = {
        "artifacts": {
            "flow_run_id": {
                "any_": [f"{context.flow_run_id}"]
            }}}

    # Perform a POST request to start the flow
    response = prefect_api_post(context, '/api/artifacts/latest/filter', parameters_json)
    assert (response.status_code >= 200) and (response.status_code < 300), \
        f'POST request ends with status {response.status_code}. Not a 2XX answer.'
    data = json.loads(response.text)
    context.steps_result = json.loads(data[0]['data'])


@then('the flow ends without error')
def step_check_flow_results(context):
    assert context.steps_result is not None, "steps_result is not set on the context environment."
    context.steps_result

    # Vérifier si tous les steps sont "OK"
    all_ok = all(step['status'] == 'OK' for step in context.steps_result)
    assert (all_ok), "Almost one step is not OK."


@then('the flow step {step:d} ends with status OK')
def step_check_flow_step(context, step: int):
    assert context.steps_result is not None

    status = 'None'
    for item in context.steps_result:
        if item['step'] == step:
            status = item['status']
            break

    assert (status == 'OK'), f"Step {step} is NOK."


@then('the flow step {step:d} ends with status NOK')
def step_check_flow_step_nok(context, step: int):
    assert context.steps_result is not None

    assert context.steps_result is not None

    status = 'None'
    for item in context.steps_result:
        if item['step'] == step:
            status = item['status']
            break

    assert (status == 'NOK'), f"Step {step} is OK."
