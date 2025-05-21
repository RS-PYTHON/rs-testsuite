from prefect import flow, task
import time
from enum import Enum
from typing import List, Tuple
from prefect.artifacts import create_markdown_artifact


class ProcessorName(Enum):
    S1_AIO = "s1-aio"
    S1_L0ASP = "s1-l0asp"
    S1_L1 = "s1-l1"
    S1_L2 = "s1-l2"



@task
def info_input(input_product_list: list[str], processor_name: ProcessorName,
               processor_version: str, processing_unit: str, dask_cluster_id: str,
               aux_collection: List[Tuple[str, str]], output_product_collection: List[Tuple[str, str]]):
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

"""
    create_markdown_artifact(
        key="input-report",
        markdown=markdown_report,
        description="Input for DPR processing"
    )


@flow
def dpr_process(input_product_list: list[str], processor_name: ProcessorName,
                processor_version: str, processing_unit: str, dask_cluster_id: str,
                aux_collection: List[Tuple[str, str]], output_product_collection: List[Tuple[str, str]]):
    time.sleep(5)
    info_input(
        input_product_list,
        processor_name,
        processor_version,
        processing_unit,
        dask_cluster_id,
        aux_collection,
        output_product_collection)


if __name__ == "__main__":
    dpr_process(["p1", "p2"], ProcessorName.S1_AIO, "1.1.0", "PU1", "cluster-id_1")
