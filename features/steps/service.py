from behave import given, when, then

import os
import requests
import json

# Call Get on the endpoint "https://" + service + "." + RS_PYTHON_URL + "/" + path
@when('the rs-python service {service} is requested with the path {path}')
def step_request_service(context: str, service: str, path: str)->str:
    # Ensure that OAuth2 authentication has been performed.
    assert context.cookies is not None, "Cookies have not be set on header."
    
    # Ensure that the RS-Python URL is defined.
    assert os.getenv("RS_PYTHON_URL"), "RS_PYTHON_URL environment variable is not set."
    
    with requests.Session() as session:
        session.cookies.update(context.cookies)

        # Construct the endpoint URL
        url = "https://" + service.lstrip('/') + "." + os.getenv("RS_PYTHON_URL").rstrip('/') + "/" + path.lstrip('/')
        headers = {"Accept": "application/json"}
        
        # Send the GET request and get the JSON response
        response = session.get(url, headers=headers)

        # Store the response status code and the response itself
        context.response_status_code = response.status_code
        context.response = response
        return response
        
# Check that the server responded with the specified status code.    
@then('the server should answer with the code {code:d}')
def step_request_code(context: str, status: int):
    assert(context.response.status_code == status), f'Status is {context.response.status_code} and not {status}.'

