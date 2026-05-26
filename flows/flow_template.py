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

from prefect import flow, task
from utils.artifacts import ReportManager

report_manager = ReportManager(4)


@task
def step1():
    report_manager.success_step(1, "Step1 description")


@task
def step2():
    report_manager.success_step(2, "Step2 description")


@task
def step3():
    report_manager.failed_step(3, "Step3 description")


@task
def step4():
    report_manager.success_step(4, "Step4 description")


@flow
def flow_template() -> str:
    # Start the 4 tasks in parallel
    future1 = step1.submit()
    future2 = step2.submit()
    future3 = step3.submit()
    future4 = step4.submit()

    # Wait all of them to finish
    future1.wait()
    future2.wait()
    future3.wait()
    future4.wait()

    # To start tasks in sequence, remove submit() and remove wait()

    report_manager.add_report_as_artefact("flow-template-test", "Template")
    return "This is a flow template"


if __name__ == "__main__":
    flow_template()
