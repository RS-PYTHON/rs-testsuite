import random
from prefect import flow, task, get_run_logger
from prefect.context import TaskRunContext
from prefect.deployments import run_deployment
import time
from  flows.utils.copernicus_enum import Station
from typing import Literal


@task(name="AIO processing session",
      description="Call DPR processor with processor AIO to compute session.")
def s1_aio(station: str, session_id: str):
    # report_manager.success_step(1, f"Start generic processing with S1-AIO on session name {session_id} on station {station}")
    task_run_ctx = TaskRunContext.get()
    task_run_ctx.task_run.name = f"Launch DPR AIO for session {session_id} on station {station}"
    run_deployment("dpr-process/dpr-process",
                   flow_run_name=f"dpr-process/dpr-process-aio-{session_id}",
                   parameters={"input_product_list": [f"{session_id}"],
                               "processor_name": "s1-aio",
                               "processor_version": "1.0.0",
                               "processing_unit": "AIO-PART",
                               "dask_cluster_id": "cluster-id_1",
                               "aux_collection": [("aux1", "my-aux-collection")],
                               "output_product_collection": [("output1", "my-product-collection")]},
                   tags=["s1", "systematic", "aio"],
                   as_subflow=True)

@task(name="Check input datatake", description="Check if the input datatake are complete.")
def check_input_datatake(dt : str):
    task_run_ctx = TaskRunContext.get()
    task_run_ctx.task_run.name = f"check segments input from catalog for datatake {dt}"
    time.sleep(1)
    if (random.randint(0, 1) == 0):
        print ("Some telemetry is misisng for datatake " + dt)
    else:
        print ("All telemetry is present for datatake " + dt + "✅")
        emit_event(mission="s1", dt=dt)
        

@task(name="Send segment event", description="Send an event to alert L0ASP.")
def emit_event(mission: str, dt: str):
    payload_json = {
        "mission": f"{mission}",
        "level": "l0",
        "type": "segment",
        "datatake": f"{dt}"
    }
    event_value = f"{mission}.segment.catalog"
    print("Send event : " + event_value)
    emit_event(event=event_value, resource={"prefect.resource.id": f"segment.{dt}"},
               payload=payload_json)


@flow (log_prints=True, validate_parameters=True)
def s1_aio_submit(station: Literal["sgs", "mti", "mps", "ins", "kse", "par", "nsg"], session_id: str):
    print("station : " + station)
    print("session_id : " + session_id)
    s1_aio(station, session_id)
    for i in range(10):
        # Générer un nombre aléatoire à 10 chiffres
        random_number = random.randint(100000000, 999999999)

        # Construire l'identifiant
        dt_id = hex(random_number)
        check_input_datatake(dt_id)
    
    

if __name__ == "__main__":
    s1_aio_submit("{}", "fake_session_name")