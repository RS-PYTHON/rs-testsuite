import random
from prefect import flow, task
from prefect.deployments import run_deployment
from datetime import datetime, timedelta
from prefect.context import TaskRunContext
import time
from prefect.artifacts import create_markdown_artifact
from  flows.utils.copernicus_enum import Station, Mission

@task 
def retrieve_last_session(station:Station):
    task_run_ctx = TaskRunContext.get()
    task_run_ctx.task_run.name = f"retrieve last sessions from {station}"
    time.sleep(random.randint(1, 2))
    
    # Obtenir la date actuelle
    date_str = datetime.now().strftime("%Y%m%d")

    # Générer un nombre aléatoire à 10 chiffres
    random_number = random.randint(1000000000, 9999999999)

    # Construire l'identifiant
    identifier = f"S1A_{date_str}{random_number}"
    start_ingestion( station, identifier)
    


@task(name="start-ingestion", description="Retrieve the list of sessions between two dates")
def start_ingestion(station: Station, session_id: str):
    time.sleep(2)
    launch_session_stage(station, session_id)


@task
def launch_session_stage(station: Station, session_id: str):
    task_run_ctx = TaskRunContext.get()
    task_run_ctx.task_run.name = f"Stage {session_id} from station {station.value}"
    run_deployment("session-stage/session-stage",
                   flow_run_name=f"stage-{session_id}-{station.value}",
                   parameters={"mission": Mission.S1, "station": station.value, "session_id": session_id,
                               "emit_event": True},
                   tags=["s1", "systematic", "ingestion"],
                   as_subflow=True)


@flow
def s1_session_retrieve(delta_time_seconds: int = 3600):
    now = datetime.now()
    before = now - timedelta(seconds=delta_time_seconds)

    markdown_report = f"""## Summary

This flow will retrieve sentinel-1 sessions from stations between two dates :
- **Start date**: {before.strftime("%Y-%m-%d %H:%M:%S")}
- **End date**: {now.strftime("%Y-%m-%d %H:%M:%S")}

"""
    create_markdown_artifact(
        key="objective",
        markdown=markdown_report,
        description="Retrieve last sessions from stations") 
    t1 = retrieve_last_session.submit(Station.MTI);
    t2 = retrieve_last_session.submit(Station.MPS);
    t3 = retrieve_last_session.submit(Station.SGS);
    t1.wait()
    t2.wait()
    t3.wait()

if __name__ == "__main__":
    s1_session_retrieve()
