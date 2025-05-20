from prefect import flow
from flows.utils.artifacts import ReportManager
import time
from enum import Enum
from typing import List, Tuple


class ProcessorName(Enum):
    S1_AIO = "s1-aio"
    S1_L0ASP = "s1-l0asp"
    S1_L1 = "s1-l1"
    S1_L2 = "s1-l2"


report_manager = ReportManager(2)


@flow
def dpr_process(input_product_list: list[str], processor_name: ProcessorName,
                processor_version: str, processing_unit: str, dask_cluster_id: str,
                aux_collection: List[Tuple[str, str]], output_product_collection: List[Tuple[str, str]]):
    time.sleep(5)


if __name__ == "__main__":
    dpr_process(["p1", "p2"], ProcessorName.S1_AIO, "1.1.0", "PU1", "cluster-id_1")
