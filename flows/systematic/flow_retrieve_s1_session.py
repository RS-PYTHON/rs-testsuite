import sys
import os
from prefect import flow, task
from utils.artifacts import ReportManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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
def flow_retrieve_s1_sessions() -> str:
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

    report_manager.add_report_as_artefact("retrieve-sentinel1-sessions", "Template")
    return "This is a flow template"


if __name__ == "__main__":
    flow_retrieve_s1_sessions()
