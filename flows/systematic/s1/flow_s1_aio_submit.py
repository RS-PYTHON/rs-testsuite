from prefect import flow, task, get_run_logger
from prefect.context import TaskRunContext
from prefect.deployments import run_deployment
import time



@task(name="AIO processing session",
      description="Call DPR processor with processor AIO to compute session.")
def s1_aio(station: str, session_id: str):
    # report_manager.success_step(1, f"Start generic processing with S1-AIO on session name {session_id} on station {station}")
    task_run_ctx = TaskRunContext.get()
    task_run_ctx.task_run.name = f"Launch DPR AIO for session {session_id} on station {station}"

    time.sleep(1)
    logger = get_run_logger()
    logger.info("station : " + station)
    logger.info("session_id : " + session_id)
    run_dpr_aio(session_id)


@task(name="launch-dpr-aio", description="Launch on-demand S1-AIO processing")
def run_dpr_aio(session_id: str):
    run_deployment("dpr-process/dpr-process",
                   flow_run_name=f"dpr-process/dpr-process-aio-{session_id}",
                   parameters={"input_product_list": [f"{session_id}"],
                               "processor_name": "s1-aio",
                               "processor_version": "1.0.0",
                               "processing_unit": "AIO-PART",
                               "dask_cluster_id": "cluster-id_1",
                               "aux_collection": [("aux1", "my-aux-collection")],
                               "output_product_collection": [("output1", "my-product-collection")]},
                   as_subflow=True)


@flow
def s1_aio_submit(station: str, session_id: str):
    s1_aio(station, session_id)


if __name__ == "__main__":
    s1_aio_submit("{}", "fake_session_name")