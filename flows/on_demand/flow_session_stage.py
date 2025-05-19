from prefect import flow, task, get_run_logger
from prefect.events import emit_event
from flows.utils.artifacts import ReportManager
import time
import random

report_manager = ReportManager(2)


@task(name="ingest-cadu-in-parallel", description="Retrieve all CADU chunks from one session")
def retrieve_all_cadus():
    report_manager.success_step(1, "Retrieve all cadus")
    tasks = [retrieve_one_cadu.submit(i) for i in range(50)]
    for t in tasks:
        t.wait()


@task(name="ingest-a-single-cadu", description="Retrieve one CADU chunk.")
def retrieve_one_cadu(i: int):
    time.sleep(random.randint(1, 5))
    report_manager.success_step(i+1, f"Retrieve cadu number {i}.")


def send_event(mission: str, station: str, session_id: str):
    payload_json = {
        "mission": f"{mission}",
        "level": "raw",
        "station": f"{station}",
        "session_ingested_id": f"{session_id}"
    }
    logger = get_run_logger()
    event_value = f"{mission}.session.ingested"
    logger.info("Send event : " + event_value)
    emit_event(event=event_value, resource={"prefect.resource.id": f"{station}.cadip"},
               payload=payload_json)


@flow
def session_stage(mission: str, station: str, session_id: str):
    retrieve_all_cadus()
    send_event(mission=mission, station=station, session_id=session_id)
    report_manager.add_report_as_artefact("retrieve-sentinel1-sessions", "retrieve sentinel-1 sessions")


if __name__ == "__main__":
    session_stage("fake_mission", "fake_station", "fake_session_name")
