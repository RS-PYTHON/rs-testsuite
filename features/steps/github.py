from behave import given, when, then
import requests

#from prefect.infrastructure.docker import DockerContainer



def check_file_exists(github_repository, filename):
    url = f"{github_repository}/{filename}"
    response = requests.get(url)
    if response.status_code == 200:
        print('OK')
        return True
    elif response.status_code == 404:
        print('NOK')
        return False
    else:
        print(f"Erreur: {response.status_code}")
        return None



@given ('the file {filename} exists on the github url {github_url}')
def step_check_github_entry(context: str, filename:str, github_url:str):
    """
    Check Github entry
    """
    assert(check_file_exists(github_url,filename))
