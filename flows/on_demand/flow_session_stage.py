from prefect import flow, task, get_run_logger
from prefect.events import emit_event
from prefect.context import TaskRunContext
from flows.utils.artifacts import ReportManager
import time
import random
from  flows.utils.copernicus_enum import Station, Mission
from typing import Literal

report_manager = ReportManager(2)


@task(description="Retrieve all CADU chunks from session {session_id}")
def retrieve_all_cadus(session_id: str, station : Station):
    task_run_ctx = TaskRunContext.get()
    task_run_ctx.task_run.name = f"Stage session {session_id} from station {station}"

    report_manager.success_step(1, "Retrieve all cadus")
    tasks = [retrieve_one_cadu.submit(i) for i in range(50)]
    for t in tasks:
        t.wait()


@task(name="ingest-a-single-cadu", description="Retrieve one CADU chunk.")
def retrieve_one_cadu(i: int):
    time.sleep(random.randint(1, 5))
    report_manager.success_step(i+1, f"Retrieve cadu number {i+1}.")


def send_event(mission: Mission, station: Station, session_id: str):
    payload_json = {
        "mission": f"{mission.value}",
        "level": "raw",
        "station": f"{station.value}",
        "session_id": f"{session_id}"
    }
    logger = get_run_logger()
    event_value = f"{mission.value}.session.ingested"
    logger.info("Send event : " + event_value)
    emit_event(event=event_value, resource={"prefect.resource.id": f"{station.value}.cadip"},
               payload=payload_json)


@flow (validate_parameters=True)
def session_stage(mission: Literal["s1", "s2", "s3"], station: Station, session_id: str):
    retrieve_all_cadus(session_id, station)
    send_event(mission=mission, station=station, session_id=session_id)
    report_manager.add_report_as_artefact("retrieve-sentinel1-sessions", "retrieve sentinel-1 sessions")


if __name__ == "__main__":
    session_stage(Mission.S1, Station.S1, "fake_session_name")
