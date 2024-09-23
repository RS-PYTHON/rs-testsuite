from prefect import flow
from prefect.runner.storage import GitRepository
import sys

# This function must be called within the cluster. From JupytherLab for example.
def deploy_flow(entrypoint:str, deployment:str, workpool:str="on-demand-k8s-pool", branch:str="feature/endpoint", github_url:str="https://github.com/RS-PYTHON/rs-testsuite.git"): 
    flow.from_source(
        source=GitRepository(
            url=github_url,
            branch=branch,
        ),
    entrypoint=entrypoint       
    ).deploy(
        name=deployment,
        work_pool_name=workpool
    )


if __name__ == "__main__":
    if ( (len(sys.argv) < 3) or (len(sys.argv) > 6)  ):
        print("Usage: python create_deployment.py <entrypoint> <deployment> [<workpool>] [<branch>] [<github_url>]")
    else:
        deploy_flow(*sys.argv[1:])

"""
   Sample: 
    python create_deployment.py flows/flow_template.py:flow_template flow-template-deployment


"""