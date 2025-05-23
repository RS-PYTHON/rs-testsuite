from prefect import flow, task
import time
from enum import Enum
from typing import List, Tuple
from prefect.artifacts import create_markdown_artifact
from  flows.utils.copernicus_enum import ProcessorName
from typing import Literal



@task
def report_info_input_processor(input_product_list: list[str], processor_name: ProcessorName,
               processor_version: str, processing_unit: str, dask_cluster_id: str,
               aux_collection: List[Tuple[str, str]], output_product_collection: List[Tuple[str, str]],
               priority: Literal["LOW", "MEDIUM", "HIGH"]):
    markdown_report = f"""# Input parameters
✅ OK
## Input parameters when calling the flow
| Parameter                     | Value                         |
|:------------------------------|:-----------------------------|
| **input_product_list**        | `{input_product_list}`        |
| **processor_name**            | `{processor_name}`            |
| **processor_version**         | `{processor_version}`         |
| **processing_unit**           | `{processing_unit}`           |
| **dask_cluster_id**           | `{dask_cluster_id}`           |
| **aux_collection**            | `{aux_collection}`            |
| **output_product_collection** | `{output_product_collection}` |
| **priority**                  | `{priority}`                  |

"""
    create_markdown_artifact(
        key="processor-configuration",
        markdown=markdown_report,
        description="Processor configuration"
    )


@task
def report_input_computed():
    time.sleep(2)
    markdown_report = f"""# Input parameters
## Here is the list of products and AUX files sent to the processor
| Kind                     | Name                         |
|:------------------------------|:-----------------------------|
| **product level 0**        | `S1A_IW_RAW__0CDV_20250423T153124_20250423T153841_058886_074C98_D8A4`        |   
| **product level 0**        | `S1A_IW_RAW__0SDV_20250423T153649_20250423T153721_058886_074C98_740D`        |
| **product level 0**        | `S1A_IW_RAW__0NDV_20250423T153124_20250423T153841_058886_074C98_431A`        |
| **product level 0**        | `S1A_IW_RAW__0ADV_20250423T153124_20250423T153841_058886_074C98_6E09`        |
| **aux file**        | `S1A_OPER_AUX_PREORB_OPOD_20250423T155530_V20250423T152424_20250423T215924`        |
| **aux file**        | `S1A_AUX_CAL_V20190228T092500_G20240327T102320.SAFE`        |
| **aux file**        | `S1A_AUX_PP1_V20190228T092500_G20241125T134138.SAFE`        |
| **aux file**        | `S1A_AUX_INS_V20190228T092500_G20190227T100643.SAFE`        |
"""
    create_markdown_artifact(
        key="input_computed",
        markdown=markdown_report,
        description="List of products and AUX files sent to the processor"
    )


@task
def report_expected():
    time.sleep(2)
    markdown_report = f"""# Input parameters
## Expected products ( output of the processor DPR)
| Product type                     |
|:------------------------------|
| **IW_GRDH__1S**        |
| **IW_SLC__1S**        |
| **IW_SLC__1A**        |
| **IW_GRDH__1A**        |

"""
    create_markdown_artifact(
        key="expected-report",
        markdown=markdown_report,
        description="Input for DPR processing"
    )


@task
def report_realised():
    time.sleep(2)
    markdown_report = f"""# Input parameters
## Input parameters when calling the flow
| Product type                     | Product name                         |
|:------------------------------|:-----------------------------|
| **IW_GRDH__1S**        | `S1A_IW_GRDH_1SDV_20250423T153652_20250423T153717_058886_074C98_9923`        |
| **IW_SLC__1S**        | `S1A_IW_SLC__1SDV_20250423T153652_20250423T153719_058886_074C98_7274`        |
| **IW_SLC__1A**        | `S1A_IW_SLC__1ADV_20250423T153652_20250423T153719_058886_074C98_6C95`        |
| **IW_GRDH__1A**        | `S1A_IW_GRDH_1ADV_20250423T153652_20250423T153717_058886_074C98_724D`        |

✅ In line with the expected products !

"""
    create_markdown_artifact(
        key="expected-report",
        markdown=markdown_report,
        description="Input for DPR processing"
    )



@flow
def dpr_process(
    input_product_list: list[str],
    processor_name: Literal["s1-aio", "s1-l0asp", "s1-l1", "s1-l2"],
    processor_version: str,
    processing_unit: str,
    dask_cluster_id: str,
    aux_collection=None,
    output_product_collection=None,
    priority: Literal["LOW", "MEDIUM", "HIGH"] = "LOW"
):
    time.sleep(5)
    report_info_input_processor(
        input_product_list,
        processor_name,
        processor_version,
        processing_unit,
        dask_cluster_id,
        aux_collection,
        output_product_collection, 
        priority)
    report_input_computed()
    report_expected()
    report_realised()


if __name__ == "__main__":
    dpr_process(["p1", "p2"], ProcessorName.S1_AIO, "1.1.0", "PU1", "cluster-id_1")
