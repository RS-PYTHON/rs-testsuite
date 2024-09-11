from behave import given, when, then
import requests
from urllib.parse import urljoin
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



    
    
    
    
    """
   def step_deploy_a_flow(context: str):
    
    Check Github entry
    
    with requests.Session() as session:
        session.cookies.update(context.cookies)

        payload = {
        "flow": {
            "name": "my_flow",
            "storage": {
                "type": "GitHub",
                "repo": "https://github.com/RS-PYTHON/rs-testsuite/tree/feature/endpoint",
                "path": "flows/hello_world.py"
            },
            "work_pool": {
                "name": "on-demand-k8s-pool"
            }}}
        prefect_server_url = "https://processing.ops.rs-python.eu"
  
        response = session.post(f"{prefect_server_url}/api/flows/",  data=json.dumps(payload))
        response = session.post(f"{prefect_server_url}/api/flows/",  data=json.dumps(payload))
        response.raise_for_status()
        print(response.status_code, flush=True)
        
        
        flow_json = {
            "name": "concombre",
            "flow_id": "68af8f2b-6d16-4d3b-9f0f-73678520ec05",
        }
        
        #response = session.get(f"{prefect_server_url}/api/health/")
        response = session.post(f"{prefect_server_url}/api/deployments/", data=json.dumps(flow_json))
        response = session.post(f"{prefect_server_url}/api/deployments/", data=json.dumps(flow_json))
        response.raise_for_status()
        print(response.status_code, flush=True)
        print (response.text, flush=True)

        assert (True)
   
   
   
   import requests
   import json

# Variables
prefect_server_url = "http://your-prefect-server-url"
api_token = "your-api-token"
github_repo_url = "https://github.com/your-repo-url"
flow_name = "your-flow-name"
work_pool_name = "your-work-pool-name"

# Headers pour l'authentification
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# Payload pour le déploiement
payload = {
    "flow": {
        "name": flow_name,
        "storage": {
            "type": "GitHub",
            "repo": github_repo_url,
            "path": "path/to/your/flow.py"
        },
        "work_pool": {
            "name": work_pool_name
        }
    }
}

# Requête POST pour déployer le flow
response = requests.post(f"{prefect_server_url}/api/flows/", headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    print("Flow déployé avec succès!")
else:
    print(f"Erreur lors du déploiement: {response.text}")

   

    
    """
    