from prefect import flow, task
from prefect.events import emit_event
from prefect.context import TaskRunContext
from prefect.deployments import run_deployment



@task(name="L1 processing slice",
      description="Call DPR processor with processor L1 to compute slice l0.")
def s1_l1(slice_l0: str, emit_event: bool):
    task_run_ctx = TaskRunContext.get()
    task_run_ctx.task_run.name = f"Launch DPR L1 for slice {slice_l0}"
    run_deployment("dpr-process/dpr-process",
                   flow_run_name=f"dpr-process/dpr-process-l1-{slice_l0}",
                   parameters={"input_product_list": [f"{slice_l0}"],
                               "processor_name": "s1-l1",
                               "processor_version": "12.8.0",
                               "processing_unit": "L1-PART",
                               "dask_cluster_id": "cluster-id_2",
                               "aux_collection": [("aux1", "my-aux-collection")],
                               "output_product_collection": [("output1", "my-product-collection")]},
                   tags=["s1", "systematic", "l1"],
                   as_subflow=True)
    if emit_event:
        send_event("074C93", "S1A_WV_SLC__1SSV_20250423T142610_20250423T145614_058885_074C93_CF43")


@task(name="Send slice event", description="Send a slice l1 event.")
def send_event(dt: str, product_name: str):
    payload_json = {
        "mission": "s1",
        "level": "l1",
        "datatake": dt,
        "slice": product_name
    }
    event_value = f"s1.slice.l1.catalog"
    print("Send event : " + event_value)
    emit_event(event=event_value, resource={"prefect.resource.id": f"slice.l1.{dt}"},
               payload=payload_json)


@flow (log_prints=True, validate_parameters=True)
def s1_l1_submit(slice_l0: str, emit_event: bool = True):
    print("input slice  : " + slice_l0)
    s1_l1(slice_l0, emit_event)
    
    
if __name__ == "__main__":
    s1_l1_submit("S1A_WV_SLC__0SSV_20250423T142610_20250423T145614_058885_074C93_CF43")