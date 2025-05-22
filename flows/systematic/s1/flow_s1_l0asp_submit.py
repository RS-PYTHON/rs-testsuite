import random
from prefect import flow, task
from prefect.events import emit_event
from prefect.context import TaskRunContext
from prefect.deployments import run_deployment
import time
from typing import Literal


@task(name="L0ASP processing segments",
      description="Call DPR processor with processor L0ASP to compute segments.")
def s1_l0asp(dt: str, emit_event: bool):
    task_run_ctx = TaskRunContext.get()
    task_run_ctx.task_run.name = f"Launch DPR L0ASP for DT {dt}"
    run_deployment("dpr-process/dpr-process",
                   flow_run_name=f"dpr-process/dpr-process-l0asp-{dt}",
                   parameters={"input_product_list": ["S1A_WV_RAW__0NSV_20250423T142609_20250423T145626_058885_074C93_7676.SAFE"
                                "S1A_WV_RAW__0ASV_20250423T142609_20250423T145626_058885_074C93_BEEA.SAFE",
                                "S1A_WV_RAW__0SSV_20250423T142609_20250423T145626_058885_074C93_3AFA.SAFE"],
                               "processor_name": "s1-l0asp",
                               "processor_version": "15.1.0",
                               "processing_unit": "L0ASP-PART",
                               "dask_cluster_id": "cluster-id_2",
                               "aux_collection": [("aux1", "my-aux-collection")],
                               "output_product_collection": [("output1", "my-product-collection")]},
                   tags=["s1", "systematic", "l0asp"],
                   as_subflow=True)
    if emit_event:
        send_event(dt, "S1A_IW_RAW__0SDV_20250423T153124_20250423T153156_058886_074C98_AF01")
        send_event(dt, "S1A_IW_RAW__0SDV_20250423T153149_20250423T153221_058886_074C98_BC89")
        send_event(dt, "S1A_IW_RAW__0SDV_20250423T153214_20250423T153246_058886_074C98_CB08")
        send_event(dt, "S1A_IW_RAW__0SDV_20250423T153239_20250423T153311_058886_074C98_6841")
        send_event(dt, "S1A_IW_RAW__0SDV_20250423T153304_20250423T153336_058886_074C98_F0A9")
        send_event(dt, "S1A_IW_RAW__0SDV_20250423T153329_20250423T153401_058886_074C98_8A94")
        send_event(dt, "S1A_IW_RAW__0SDV_20250423T153354_20250423T153426_058886_074C98_65FE")
        send_event(dt, "S1A_IW_RAW__0SDV_20250423T153419_20250423T153451_058886_074C98_5C9F")
        send_event(dt, "S1A_IW_RAW__0SDV_20250423T153444_20250423T153516_058886_074C98_1BB1")
        send_event(dt, "S1A_IW_RAW__0SDV_20250423T153509_20250423T153541_058886_074C98_5D09")
        send_event(dt, "S1A_IW_RAW__0SDV_20250423T153534_20250423T153606_058886_074C98_38D4")
        send_event(dt, "S1A_IW_RAW__0SDV_20250423T153559_20250423T153631_058886_074C98_6E98")
        send_event(dt, "S1A_IW_RAW__0SDV_20250423T153624_20250423T153656_058886_074C98_B9A6")    
        send_event(dt, "S1A_IW_RAW__0SDV_20250423T153649_20250423T153721_058886_074C98_740D")
        send_event(dt, "S1A_IW_RAW__0SDV_20250423T153714_20250423T153746_058886_074C98_CDCB")
        send_event(dt, "S1A_IW_RAW__0SDV_20250423T153739_20250423T153811_058886_074C98_D607")
        send_event(dt, "S1A_IW_RAW__0SDV_20250423T153804_20250423T153841_058886_074C98_A0C2")


@task(name="Send slice event", description="Send a slice event to alert level 1 and level 2.")
def send_event(dt: str, product_name: str):
    payload_json = {
        "mission": "s1",
        "level": "l0",
        "datatake": dt,
        "slice": product_name
    }
    event_value = f"s1.slice.l0.catalog"
    print("Send event : " + event_value)
    emit_event(event=event_value, resource={"prefect.resource.id": f"slice.l0.{dt}"},
               payload=payload_json)


@flow (log_prints=True, validate_parameters=True)
def s1_l0asp_submit(datatake: str, emit_event: bool = True):
    print("datatake : " + datatake)
    s1_l0asp(datatake, emit_event)
    
    
if __name__ == "__main__":
    s1_l0asp_submit("074C93")