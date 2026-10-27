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
import boto3
from behave import given, then, when
from botocore.exceptions import ClientError, NoCredentialsError

URL = "https://api.github.com/repos/RS-PYTHON/rs-client-libraries/actions/workflows/benchmark-processor.yml" #to update

def _headers():
    return {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}#to adapt



#first minimal version
@given("the branch is {branch}")
def step_branch_is_correct(context, branch):
    context.branch=value

@given("the cluster is {cluster}")
def step_cluster_is_correct(context, cluster):
    context.cluster=cluster

@given("the processor is {processor}")
def step_processor_is_correct(context, processor):
    context.processor=processor

@given("the precessor version is {processor_version}")
def step_processor_version_is_correct(context, processor_version):
    context.processor_version=processor_version

@given("the scenario is {scenario}")
def step_scenario_is_correct(context, scenario):
    context.scenario=scenario

@given("the keycloak username is {keycloak_username}")
def step_keycloak_username_is_correct(context, keycloak_username):
    context.keycloak_username=keycloak_username


@when ("the benchmark workflow is launched")
def launch_benchmark(context):
    inputs = {
        "cluster": context.cluster,
        "processor": context.processor,
        "processor_version" : context.processor_version,
        "scenario" : context.scenario,
        "kecloak_username" : context.kecloak_username
    }
    resp = requests.post(URL + "/dispaches", headers = _headers(), json = {"ref": context.branch, "inputs": inputs})
    assert resp.status_code == 204 , resp.text
    #sleep ?
    time.sleep(10)
    runs = requests.get (URL + "/runs", headers = _headers(), params = {"branch":context.branch, "per_page": 1}).json()
    context.run_id = runs["workflow_runs"][0]["id"]


@then ("the benchmark workflow run succeeds")
def check_benchmark(context):
    run_url = f"https://api.github.com/repos/RS-PYTHON/rs-client-libraries/actions/runs/{context.run_id}"
    run = requests.get(run_url, headers=_headers()).json()
    while run["status"] != "completed":
        time.sleep(30)
        run = requests.get(run_url, headers=_headers()).json()
    assert run["conclusion"] == "success", run["html_url"]



