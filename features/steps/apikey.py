from behave import given, when, then
from behave import use_step_matcher
import hashlib
import os
import requests
import uuid
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.parse import urljoin


@given('user {user:d} is defined')
def step_define_user(context, user: int):
    """Checks that user credentials are defined as environment variables"""
    assert f'RSPY_TEST_USER_{user}' in os.environ, f"RSPY_TEST_USER_{user} environment variable is not set."
    assert f'RSPY_TEST_PASS_{user}' in os.environ, f"RSPY_TEST_PASS_{user} environment variable is not set."

    context.login = os.getenv(f'RSPY_TEST_USER_{user}')
    context.passw = os.getenv(f'RSPY_TEST_PASS_{user}')

@given('he is logged in')
def step_login(context):
    assert os.getenv("APIKEY_URL") is not None, "APIKEY_URL environment variable is not set."
    step_login_into_url(context,os.getenv("APIKEY_URL"))


@given('he is logged in on url {url}')
def step_login_into_url(context, url : str):
    """Login to keycloak"""
    assert url is not None, "url parameter is missing."
    assert context.login is not None, "Login has not be added to the set on the request header."
    assert context.passw is not None, "Password has not be added to the set on the request header."

    with requests.Session() as session:
        # Step 1: Connect to API key manager to be redirected to URL login form
        response = session.get(url)
        #response = session.get(os.getenv("APIKEY_URL"))
        response.raise_for_status()

        # Step 2: Parse html login form
        form = BeautifulSoup(response.content, 'html.parser').find('form')
        form_data = {input_tag['name']: input_tag.get('value', '') for input_tag in form.find_all('input')}

        # Fill form with user credentials
        form_data['username'] = context.login
        form_data['password'] = context.passw

        # Step 3: Submit form to get authorization code
        response = session.post(form['action'], data=form_data)
        response.raise_for_status()

        # Step 4: Perform redirect
        redirect_url = response.url
        response = session.get(redirect_url)
        response.raise_for_status()

        # Save cookies to be authenticated in future sessions
        context.cookies = session.cookies


use_step_matcher("re")

@when('he creates a new (?P<key_type>permanent|temporary) API key')
def step_create_apikey(context, key_type: str):
    """Create a new API key"""
    assert "APIKEY_URL" in os.environ, "APIKEY_URL environment variable has not been set."
    assert context.cookies is not None, "Cookies are missing on context."

    with requests.Session() as session:
        session.cookies.update(context.cookies)

        # Create new API key
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        name = f'test_{now}'
        never_expires = True if "permanent" == key_type else False

        url = f'{os.getenv("APIKEY_URL")}/auth/api_key/new?name={name}&never_expires={never_expires}'
        response = session.get(url)
        assert(response.status_code == 200), f'status for GET {url} is {response.status_code} and not 200'
        
        
        # Save API key
        context.apikey = response.json()
        assert context.apikey is not None, "apikey cannot be retrieve from request answer."
        assert uuid.UUID(context.apikey) is not None


use_step_matcher("parse")

@when('he revokes the last created API key')
def step_revoke_apikey(context: str):
    """Revoke the last created API key"""
    assert "APIKEY_URL" in os.environ, "APIKEY_URL environment variable has not been set."
    assert context.cookies is not None, "Cookies are missing on context."
    assert context.apikey is not None, "apikey cannot be retrieve from request answer."
    assert uuid.UUID(context.apikey) is not None

    with requests.Session() as session:
        session.cookies.update(context.cookies)

        # Revoke the last created API key             
        response = session.get(urljoin(os.getenv("APIKEY_URL"),
            f'/auth/api_key/revoke?api-key={context.apikey}'))
        response.raise_for_status()
 

@then('the last created API key should be revoked')
def step_check_revocation_apikey(context):
    """Check API key existence and validity"""
    assert "APIKEY_URL" in os.environ, "APIKEY_URL environment variable has not been set."
    assert context.cookies is not None, "Cookies are missing on context."
    assert context.apikey is not None, "apikey cannot be retrieve from request answer."
    assert uuid.UUID(context.apikey) is not None

    with requests.Session() as session:
        session.cookies.update(context.cookies)

        response = session.get(urljoin(os.getenv("APIKEY_URL"), '/auth/api_key/list'))
        response.raise_for_status()

        hash_hex = encode_sha_256(context.apikey)

        valid_key_found = False
        for key in response.json():
            if key['api_key'] == hash_hex:
                assert key['is_active'] == False, "Key is still active."
                valid_key_found = True

    assert valid_key_found



@then('the API key should be valid')
def step_check_apikey(context):
    """Check API key existence and validity"""
    assert "APIKEY_URL" in os.environ, "APIKEY_URL environment variable has not been set."
    assert context.cookies is not None, "Cookies are missing on context."
    assert context.apikey is not None, "apikey cannot be retrieve from request answer."
    assert uuid.UUID(context.apikey) is not None

    with requests.Session() as session:
        session.cookies.update(context.cookies)

        response = session.get(urljoin(os.getenv("APIKEY_URL"), '/auth/api_key/list'))
        response.raise_for_status()

        
        hash_hex = encode_sha_256(context.apikey)
        
        valid_key_found = False
        for key in response.json():
            if key['api_key'] == hash_hex:
                assert key['is_active'] == True, "Key is inactive."
                valid_key_found = True

    assert valid_key_found, "No valid key has been found"

"""
Step to ensure that the API-KEY is set on environment variable.
We will avoid to create an API-KEY for each test.
There is a dedicated test to check API-KEY creation.
"""
@given('user {user:d} has got an apikey')
def step_check_apikey(context, user: int):
    """Checks that user APIKEY is set on environment variable"""
    assert f'RSPY_TEST_APIK_{user}' in os.environ, f"RSPY_TEST_APIK_{user} environment varibale has not been set."
    context.apikey = os.getenv(f'RSPY_TEST_APIK_{user}')
    
    
def encode_sha_256 (key:str)->str:
    chaine_bytes = key.encode('utf-8')
    hash_obj = hashlib.sha256(chaine_bytes)
    return hash_obj.hexdigest()
