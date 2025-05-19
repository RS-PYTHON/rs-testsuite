from prefect import flow, task, get_run_logger
from prefect.events import emit_event
from flows.utils.artifacts import ReportManager
# from prefect.deployments import run_deployment
import time

report_manager = ReportManager(2)


@task(name="launch-s1-aio", description="Launch S1 AIO processing")
def s1_aio(param1, param2):
    #report_manager.success_step(1, f"Start generic processing with S1-AIO on session name {session_id} on station {station}")
    time.sleep(1)
    logger = get_run_logger()
    logger.info("param1" + param1)
    logger.info("param2" + param2)
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
def s1_aio_submit(param1, param2):
    s1_aio(param1, param2)


if __name__ == "__main__":
    s1_aio_submit("fake_station", "fake_session_name")
