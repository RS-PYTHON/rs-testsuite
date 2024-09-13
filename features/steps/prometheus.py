from behave import given, when, then

import os
import requests
import json

@when('we call the prometheus query {query}')
def step_request_prometheus(context: str, query: str):
    """
    Call Prometheus query
    """
    step_request_service(context, 'monitoring', 'prometheus/api/v1/query?query=' + query)

@then('almost one prometheus result is provided')
def step_check_prometheus_result(context: str):
    """
    Check Prometheus response
    """
    step_check_json_prometheus_is_not_null(context, 'data', 'result')

@when('the rs-python service {service} is requested with the path {path}')
def step_request_service(context: str, service: str, path: str):
    """
    This step calls the endpoint "https://" + service + "." + RS_PYTHON_URL + "/" + path
    and records the status code.
    """
    # Ensure that OAuth2 authentication has been performed.
    assert context.cookies is not None
    
    # Ensure that the RS-Python URL is defined.
    assert os.getenv("RS_PYTHON_URL") is not None
    
    with requests.Session() as session:
        session.cookies.update(context.cookies)

        # Construct the endpoint URL
        url = "https://" + service.lstrip('/') + "." + os.getenv("RS_PYTHON_URL").rstrip('/') + "/" + path.lstrip('/')
        print(f"url {url}")
        
        headers = {
            "Accept": "application/json"
        }
        
        # Send the GET request and get the JSON response
        response = session.get(url, headers=headers)
        response.raise_for_status()

        # Store the response status code and the response itself
        context.response_status_code = response.status_code
        context.response = response

@then('the server should answer with the code {code:d}')
def step_request_code(context: str, code: int):
    """
    Check that the server responded with the specified status code.
    """
    assert context.response_status_code == code

def is_valid_json(chain: str):
    try:
        json.loads(chain)
        return True
    except:
        return False

@then('the answer is a json with almost one element on the path {level1}.{level2}')
def step_check_json_prometheus_is_not_null(context: str, level1: str, level2: str):
    """
    Specific check: Ensure the response is in JSON format and that the path level1.level2 contains at least one element.
    """
    assert context.response_status_code == 200
    assert is_valid_json(context.response.text) == True

    data = json.loads(context.response.text)
    assert len(data[level1][level2]) > 0
