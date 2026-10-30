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
import time

import requests
from behave import given, then, when

# base URL
URL = "https://api.github.com/repos/RS-PYTHON/rs-client-libraries/actions/workflows/benchmark-processor.yml"


def _headers():
    """
    the github authentication secret
    """
    return {
        "Authorization": f"Bearer {os.environ['TOKEN_ACTION_RS_CLIENT_LIBRAIRIES']}",
    }


"""
each parameter is configurable in jira
the possible combinations can be found in rs-client-libraries -> benchmark processor
"""


@given("user {user:d} is defined")
def step_define_user(context, user: int):
    """Checks that user credentials are defined as environment variables"""
    assert (
        f"RSPY_TEST_USER_{user}" in os.environ
    ), f"RSPY_TEST_USER_{user} environment variable is not set."
    assert (
        f"RSPY_TEST_PASS_{user}" in os.environ
    ), f"RSPY_TEST_PASS_{user} environment variable is not set."

    context.keycloak_user = os.getenv(f"RSPY_TEST_USER_{user}")


@given('the branch is "{branch}"')
def step_branch(context, branch):
    """the github branch (repo client-libraries)"""
    context.branch = branch


@given('the cluster is "{cluster}"')
def step_cluster(context, cluster):
    """the cluster (dev/ops)"""
    context.cluster = cluster


@given('the processor is "{processor_name}"')
def step_processor(context, processor_name):
    """the processor to benchmark (eg : s3_l0)"""
    context.processor_name = processor_name


@given('the processor version is "{processor_version}"')
def step_processor_version(context, processor_version):
    """the version of the processor (eg : 1.5.0)"""
    context.processor_version = processor_version


@given('the scenario is "{benchmark_scenario}"')
def step_scenario(context, benchmark_scenario):
    """the scenario A/B"""
    context.benchmark_scenario = benchmark_scenario


@when("the benchmark workflow is launched")
def launch_benchmark(context):
    """launch the benchmark processor and get the run id"""
    inputs = {
        "cluster": context.cluster,  # the kubernetes cluster (ops/dev)
        "processor_name": context.processor_name,
        "processor_version": context.processor_version,
        "scenario": context.benchmark_scenario,
        "keycloak_user": context.keycloak_user,
    }
    resp = requests.post(
        URL + "/dispatches",
        headers=_headers(),
        json={"ref": context.branch, "inputs": inputs, "return_run_details": True},
        timeout=30,
    )
    assert resp.status_code == 200, resp.text
    # The dispatch API returns the id of the run it created, so we follow exactly this run
    context.run_id = resp.json()["workflow_run_id"]


@then("the benchmark workflow run succeeds")
def check_benchmark(context):
    """wait until the benchmark finishes and check that it succeeded"""
    run_url = f"https://api.github.com/repos/RS-PYTHON/rs-client-libraries/actions/runs/{context.run_id}"
    run = requests.get(run_url, headers=_headers(), timeout=30).json()
    while run["status"] != "completed":
        time.sleep(30)
        run = requests.get(run_url, headers=_headers(), timeout=30).json()
    assert run["conclusion"] == "success", run["html_url"]
