# Copyright 2023-2026 Airbus
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from behave import then, when
from requests import Response, Session


# Call Get on the endpoint "https://" + service + "." + RS_PYTHON_URL + "/" + path
@when("the rs-python service {service} is requested with the path {path}")
def step_request_service(context, service: str, path: str) -> Response:
    # Ensure that OAuth2 authentication has been performed.
    assert context.cookies is not None, "Cookies have not be set on header."

    # Ensure that the RS-Python URL is defined.
    assert os.getenv("RS_PYTHON_URL"), "RS_PYTHON_URL environment variable is not set."

    with Session() as session:
        session.cookies.update(context.cookies)

        # Construct the endpoint URL
        url = (
            "https://"
            + service.lstrip("/")
            + "."
            + os.environ["RS_PYTHON_URL"].rstrip("/")
            + "/"
            + path.lstrip("/")
        )
        headers = {"Accept": "application/json"}

        # Send the GET request and get the JSON response
        response = session.get(url, headers=headers)

        # Store the response status code and the response itself
        context.response_status_code = response.status_code
        context.response = response
        return response


# Check that the server responded with the specified status code.
@then("the server should answer with the code {code:d}")
def step_request_code(context, status: int):
    assert (
        context.response.status_code == status
    ), f"Status is {context.response.status_code} and not {status}."
