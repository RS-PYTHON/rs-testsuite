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

import requests
from behave import given
from behave.runner import Context


def check_file_exists(github_repository: str, filename: str):
    """
    Checks if a file exists in the specified GitHub repository.

    Args:
        github_repository (str): The URL of the GitHub repository.
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file exists, False if the file does not exist,
                None if there is an error other than 404.
    """
    url = f"{github_repository}/{filename}"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        print("OK")
        return True
    if response.status_code == 404:
        print("NOK")
        return False
    print(f"Error: {response.status_code}")
    return None


@given("the file {filename} exists on the github url {github_url}")
def step_check_github_entry(context: Context, filename: str, github_url: str):
    """
    Step definition to check if a file exists in the specified GitHub repository.

    Args:
        context (Context): The context object provided by Behave.
        filename (str): The name of the file to check.
        github_url (str): The URL of the GitHub repository.

    Asserts:
        The file exists in the specified GitHub repository.
    """
    assert context is not None
    assert check_file_exists(
        github_url,
        filename,
    ), f"The file {filename} cannot be found on GitHub url {github_url}."
