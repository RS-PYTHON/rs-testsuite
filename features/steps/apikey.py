"""API Key test steps"""

from behave import given, when, then
from behave import use_step_matcher

import os
import requests
import uuid
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.parse import urljoin


@given('user {user:d} is defined')
def step_define_user(context, user: int):
    """Checks that user credentials are defined as environment variables"""
    assert f'RSPY_TEST_USER_{user}' in os.environ
    assert f'RSPY_TEST_PASS_{user}' in os.environ

    context.login = os.getenv(f'RSPY_TEST_USER_{user}')
    context.passw = os.getenv(f'RSPY_TEST_PASS_{user}')


@given('XXXhe is logged in')
def step_login(context):
    assert "APIKEY_URL" in os.environ
    step_login_into_url(context,os.getenv("APIKEY_URL"))


@given('he is logged in on url {url}')
def step_login_into_url(context, url : str):
    """Login to keycloak"""
    assert url is not None
    assert context.login is not None
    assert context.passw is not None

    with requests.Session() as session:
        # Step 1: Connect to API key manager to be redirected to Keycloak login form
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
    assert "APIKEY_URL" in os.environ
    assert context.cookies is not None

    with requests.Session() as session:
        session.cookies.update(context.cookies)

        # Create new API key
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        name = f'test_{now}'
        never_expires = True if "permanent" == key_type else False

        response = session.get(urljoin(os.getenv("APIKEY_URL"),
            f'/auth/api_key/new?name={name}&never_expires={never_expires}'))
        response.raise_for_status()
        
        
        # Save API key
        context.apikey = response.json()
        assert context.apikey is not None
        assert uuid.UUID(context.apikey) is not None


use_step_matcher("parse")

@when('he revokes the last created API key')
def step_revoke_apikey(context: str):
    """Revoke the last created API key"""
    assert "APIKEY_URL" in os.environ
    assert context.cookies is not None
    assert context.apikey is not None
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
    assert "APIKEY_URL" in os.environ
    assert context.cookies is not None
    assert context.apikey is not None
    assert uuid.UUID(context.apikey) is not None

    with requests.Session() as session:
        session.cookies.update(context.cookies)

        response = session.get(urljoin(os.getenv("APIKEY_URL"), '/auth/api_key/list'))
        response.raise_for_status()

        valid_key_found = False
        for key in response.json():
            if key['api_key'] == context.apikey:
                assert key['is_active'] == False
                valid_key_found = True

    assert valid_key_found



@then('the API key should be valid')
def step_check_apikey(context):
    """Check API key existence and validity"""
    assert "APIKEY_URL" in os.environ
    assert context.cookies is not None
    assert context.apikey is not None
    assert uuid.UUID(context.apikey) is not None

    with requests.Session() as session:
        session.cookies.update(context.cookies)

        response = session.get(urljoin(os.getenv("APIKEY_URL"), '/auth/api_key/list'))
        response.raise_for_status()

        valid_key_found = False
        for key in response.json():
            if key['api_key'] == context.apikey:
                assert key['is_active'] == True
                valid_key_found = True

    assert valid_key_found
