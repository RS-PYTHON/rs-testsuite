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

import boto3
from behave import given, then, when
from botocore.exceptions import ClientError, NoCredentialsError




#copy of another test
@given("user {user:d} is defined")
def step_define_user(context, user: int):
    """Checks that user credentials are defined as environment variables"""
    assert (
        f"RSPY_TEST_USER_{user}" in os.environ
    ), f"RSPY_TEST_USER_{user} environment variable is not set."
    assert (
        f"RSPY_TEST_PASS_{user}" in os.environ
    ), f"RSPY_TEST_PASS_{user} environment variable is not set."

    context.login = os.getenv(f"RSPY_TEST_USER_{user}")
    context.passw = os.getenv(f"RSPY_TEST_PASS_{user}")


#first minimal version
@given("the branch is {branch}")
def step_branch_is_correct(context, value):
    context.branch=value

@given("the cluster is {cluster}")
def step_cluster_is_correct(context, value):
    context.cluster=value

@given("the processor is {processor}")
def step_processor_is_correct(context, value):
    context.processor=value

@given("the precessor version is {processor_version}")
def step_processor_version_is_correct(context, value):
    context.processor_version=value

@given("the scenario is {scenario}")
def step_scenario_is_correct(context, value):
    context.scenario=value

@given("the keycloak username is {keycloak_username}")
def step_keycloak_username_is_correct(context, value):
    context.keycloak_username=value

#TODO
@when ("the benchmark workflow is launched")
def launch_benchmark(context):
    assert (context.branch == "develop")
    assert (context.cluster == "ops")
    assert (context.processor == "s3_l0")
    assert (context.processor_version == "1.5.0")
    assert (context.scenario == "B")
    assert (context.keycloak_username == "test_username")

#TODO
@then ("the benchmark workflow run succeeds")
def check_benchmark(context):
    return True


