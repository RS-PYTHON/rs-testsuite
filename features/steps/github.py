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
