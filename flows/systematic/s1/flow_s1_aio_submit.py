from prefect import flow, task, get_run_logger
from prefect.events import emit_event
from flows.utils.artifacts import ReportManager
# import json
# from prefect.deployments import run_deployment
import time

report_manager = ReportManager(2)


@task(name="AIO processing session {session_id}", description="Call DPR processor with processor AIO to compute session {session_id}")
def s1_aio(station: str, session_id: str):
    # report_manager.success_step(1, f"Start generic processing with S1-AIO on session name {session_id} on station {station}")
    time.sleep(1)
    logger = get_run_logger()
    logger.info("station : " + station)
    logger.info("session_id : " + session_id)
    send_event(2, "station", "session_id")


def send_event(step, station, session_id):
    payload_json = {
        "mission": "s1",
        "level": "raw",
        "processor": "s1-aio",
        "station": f"{station}",
        "session_id": f"{session_id}"
    }
    # prefect.resource.name  emit_event(event=f"{name}.sent.event!", resource={"prefect.resource.id": f"coder.{name}"})

    emit_event(event="s1.aio.start", resource={"prefect.resource.id": "s1.aio"}, payload=payload_json)
    report_manager.success_step(step, f"Start AIO event for session {session_id}")


@flow
def s1_aio_submit(station: str, session_id: str):
    s1_aio(station, session_id)


if __name__ == "__main__":
    s1_aio_submit("{}", "fake_session_name")
