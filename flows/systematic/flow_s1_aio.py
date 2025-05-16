from prefect import flow, task
from prefect.events import emit_event
from datetime import datetime, timedelta
from flows.utils.artifacts import ReportManager
import time

report_manager = ReportManager(2)


@task(name="launch-connection", description="Connect to the station")
def s1_aio(station: str, session_id: str):
    report_manager.success_step(1, f"Start generic processing with S1-AIO on session name {session_id}")
    time.sleep(1)
    send_event(2, station, session_id)


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
def s1_aio_start(station: str, session_id: str):
    s1_aio(session_id)

if __name__ == "__main__":
    s1_aio_start("fake_station", "fake_session_name")