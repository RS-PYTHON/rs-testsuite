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

import logging

from behave import then
from rs_server import rs_server_get, rs_server_post

logger = logging.getLogger(__name__)


@then("staging get url succeeds")
def step_check_staging(context):
    """
    Check the staging url
    """
    rs_server_get(context, "processes/staging", 200)


@then("staging post url exists")
def step_check_staging_post(context):
    """
    Check the staging url
    """
    process_json: dict = {}
    # logger.info("JSON use for POST Staging request : %s", process_json)
    rs_server_post(context, "processes/staging/execution", process_json, 422)
