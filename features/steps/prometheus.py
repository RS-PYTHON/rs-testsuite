from behave import given, when, then
from behave import use_step_matcher

import os
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.parse import urljoin


@when('we call the prometheus query {query}')
def step_request_prometheus(context: str, query:str):
    """
    Call prometheus query
    """
    step_request_service(context, 'monitoring', 'prometheus/api/v1/query?query=' + query)


@then ('almost one prometheus result is provided')
def step_check_prometheus_result(context: str):
    """
    Check Prometheus answer
    """
    step_check_json_prometheus_is_not_null (context, 'data', 'result')



@when('the rs-python service {service} is requested with the path {path}')
def step_request_service(context: str, service:str, path:str):
    """    
    This step call the endpoint "https://" + service + "." + RS_PYTHON_URL + "/" + path
    and register the status code.
    
    """
    # Check that the oauth2 authentication has been held.
    assert context.cookies is not None
    
    # Check that RS-Python path is defined
    assert os.getenv("RS_PYTHON_URL") is not None
    

    with requests.Session() as session:
        session.cookies.update(context.cookies)

        # Call the endpoint
        url = "https://" + service.lstrip('/') + "." + os.getenv("RS_PYTHON_URL").rstrip('/') + "/" + path.lstrip('/')
        print(f"url {url}")
        
        headers = {
        "Accept": "application/json"
        }
        
        # There is a need to perform the request twice
        # The first time, we get redirected to the home page of the service (we test prometheus)
        # The second time we get the JSON data result
        response = session.get(url, headers=headers)
        response = session.get(url, headers=headers)
        response.raise_for_status()

        # Store the result
        context.response_status_code = response.status_code
        context.response = response

        

@then('the server should answer with the code {code:d}')
def step_request_code(context: str, code:int):
    """
    Check that the Server has answered with a given status code.
    """
    assert (context.response_status_code == code)
        

def is_valid_json(chain:str):
    try:
        json.loads(chain)
        return True
    except :
        return False
    

@then ('the answer is a json with almost one element on the path {level1}.{level2}')
def step_check_json_prometheus_is_not_null(context: str, level1:str, level2:str):
    """
    Very specific check. Check that the answer is on JSON format and the level1.level2 is a list of almost one element.
    """
    assert context.response_status_code == 200
    assert (is_valid_json(context.response.text)==True)

    data = json.loads (context.response.text )
    assert len(data[level1][level2])> 0
    
    
