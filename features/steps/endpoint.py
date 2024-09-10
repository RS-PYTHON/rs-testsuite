from behave import given, when, then
from behave import use_step_matcher

import os
import requests
import uuid
import json
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.parse import urljoin


@when('the rs-python service {service} is requested with the path {path}')
def step_request_service(context: str, service:str, path:str):
    """    
    This step call the endpoint "https://" + service + "." + RS_PYTHON_URL + "/" + path
    and register the status code.
    
    """
    # Check that the user environment variables are set
    assert context.login is not None
    assert context.passw is not None
    
    # Check that the oauth2 authentication has been held.
    assert context.cookies is not None
    
    # Check that RS-Python path is defined
    assert os.getenv("RS_PYTHON_URL") is not None
    

    with requests.Session() as session:
        session.cookies.update(context.cookies)

        # Call the endpoint
        url = "https://" + service.lstrip('/') + "." + os.getenv("RS_PYTHON_URL").rstrip('/') + "/" + path.lstrip('/')
        print(f"url {url}")
        response = session.get(url)
        print(response.text)
        response.raise_for_status()

        # Store the result
        context.response_status_code = response.status_code
        context.response = response.text
        print()

        
        

@then('the server should answer with the code {code:d}')
def step_request_service(context: str, code:int):
    """
    Check that the Server has answered with a given status code.
    
    """
    # Check that the request has been sent to the server
    assert context.response_status_code is not None
    
    # check the server answer
    assert (context.response_status_code == code)
        

def is_valid_json(chain:str):
    print(f"test de la chaine {chain}.")
    try:
        json.loads(chain)
        print("c'est OK")
        return True
    except :
        print("c'est pas OK")
        return False
    

@then ('the answer is a json with almost one element on the path {level1}.{level2}')
def step_check_json_prometheus_is_not_null(context: str, level1:str, level2:str):
    """
    Very specific check. Check that the answer is on JSON format and the level1.level2 is a list of almost one element.
    """
    assert context.response_status_code is not None
    # Only answwer 200 are taken into account (which make previous step un-usefull)
    assert context.response_status_code == 200
    assert (is_valid_json(context.response)==True)
    
    data = context.response.json
    assert len(data[level1][level2])> 0
    
    
