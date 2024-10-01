from behave import given
import requests


def check_file_exists(github_repository, filename):
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
    response = requests.get(url)
    if response.status_code == 200:
        print('OK')
        return True
    elif response.status_code == 404:
        print('NOK')
        return False
    else:
        print(f"Error: {response.status_code}")
        return None


@given('the file {filename} exists on the github url {github_url}')
def step_check_github_entry(context: str, filename: str, github_url: str):
    """
    Step definition to check if a file exists in the specified GitHub repository.

    Args:
        context (str): The context object provided by Behave.
        filename (str): The name of the file to check.
        github_url (str): The URL of the GitHub repository.

    Asserts:
        The file exists in the specified GitHub repository.
    """
    assert (check_file_exists(github_url, filename)), f"The file {filename} cannot be found on GitHub url {github_url}."
