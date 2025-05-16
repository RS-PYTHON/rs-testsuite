"""
Sample:
!python create_deployment.py flows/systematic/flow_retrieve_s1_session.py:retrieve_s1_list_of_sessions s1-retrieve-sessions s1,raw,systematic
!python create_deployment.py flows/flow_template.py:flow_template flow_template
"""

import sys

from prefect import flow
from prefect.runner.storage import GitRepository


# This function must be called within the cluster. From JupytherLab for example.
def deploy_flow(
    entrypoint: str,
    deployment: str,
    tags: list[str],
    workpool: str = "systematic-processing-pool",
    branch: str = "feat/systematic-processing",
    github_url: str = "https://github.com/RS-PYTHON/rs-testsuite.git",
):
    flow.from_source(
        source=GitRepository(
            url=github_url,
            branch=branch,
        ),
        entrypoint=entrypoint,
    ).deploy(name=deployment, work_pool_name=workpool, tags=tags)


if __name__ == "__main__":
    if (len(sys.argv) < 4) or (len(sys.argv) > 6):
        print(
            "Usage: python create_deployment.py <entrypoint> <deployment> <tags(comma-separated)> [<workpool>] [<branch>] [<github_url>]",
        )
    else:
        entrypoint = sys.argv[1]
        deployment = sys.argv[2]
        tags = sys.argv[3].split(",") 
        deploy_flow(entrypoint, deployment, tags, *sys.argv[4:])