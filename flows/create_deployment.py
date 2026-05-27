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

"""
Sample:
python create_deployment.py flows/flow_template.py:flow_template flow-template-deployment
"""

import sys

from prefect import flow
from prefect.runner.storage import GitRepository


# This function must be called within the cluster. From JupytherLab for example.
def deploy_flow(
    entrypoint: str,
    deployment: str,
    workpool: str = "on-demand-k8s-pool",
    branch: str = "feature/endpoint",
    github_url: str = "https://github.com/RS-PYTHON/rs-testsuite.git",
):
    flow.from_source(
        source=GitRepository(
            url=github_url,
            branch=branch,
        ),
        entrypoint=entrypoint,
    ).deploy(name=deployment, work_pool_name=workpool)


if __name__ == "__main__":
    if (len(sys.argv) < 3) or (len(sys.argv) > 6):
        print(
            "Usage: python create_deployment.py <entrypoint> <deployment> [<workpool>] [<branch>] [<github_url>]",
        )
    else:
        deploy_flow(*sys.argv[1:])
