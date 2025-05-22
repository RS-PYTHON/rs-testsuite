from prefect import flow, task
from prefect.events import emit_event
from prefect.context import TaskRunContext
from prefect.deployments import run_deployment


@task(name="L2 processing slice",
      description="Call DPR processor with processor L2 to compute slice l0.")
def s1_l2(slice_l0: str, emit_event: bool):
    task_run_ctx = TaskRunContext.get()
    task_run_ctx.task_run.name = f"Launch DPR L2 for slice {slice_l0}"
    run_deployment("dpr-process/dpr-process",
                   flow_run_name=f"dpr-process/dpr-process-l2-{slice_l0}",
                   parameters={"input_product_list": [f"{slice_l0}"],
                               "processor_name": "s1-l2",
                               "processor_version": "22.4.0",
                               "processing_unit": "L2-PART",
                               "dask_cluster_id": "cluster-id_2",
                               "aux_collection": [("aux1", "my-aux-collection")],
                               "output_product_collection": [("output1", "my-product-collection")]},
                   tags=["s1", "systematic", "l2"],
                   as_subflow=True)
    if emit_event:
        send_event("074C93", "S1A_WV_SLC__2SSV_20250332T142610_20250423T145614_056895_074C93_ED09")


@task(name="Send slice event", description="Send a slice l2 event.")
def send_event(dt: str, product_name: str):
    payload_json = {
        "mission": "s1",
        "level": "l2",
        "datatake": dt,
        "slice": product_name
    }
    event_value = f"s1.slice.l2.catalog"
    print("Send event : " + event_value)
    emit_event(event=event_value, resource={"prefect.resource.id": f"slice.l2.{dt}"},
               payload=payload_json)


@flow (log_prints=True, validate_parameters=True)
def s1_l2_submit(slice_l0: str, emit_event: bool = True):
    print("input slice  : " + slice_l0)
    s1_l2(slice_l0, emit_event)
    
    
if __name__ == "__main__":
    s1_l2_submit("S1A_WV_SLC__0SSV_20250423T142610_20250423T145614_058885_074C93_CF43")