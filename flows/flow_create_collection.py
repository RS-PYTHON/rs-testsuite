# Set logger level to info
import logging
import os
from datetime import datetime
import rs_common
from prefect import flow, task
from prefect.blocks.system import Secret
from pystac import Collection, Extent, SpatialExtent, TemporalExtent
from rs_client.rs_client import RsClient
from utils.artifacts import ReportManager

rs_server_href = os.environ["RSPY_WEBSITE"]
report_manager = ReportManager(2)
rs_common.logging.Logging.level = logging.INFO


@task
def step1():
    secret_block = Secret.load("validator-api-key")
    apikey1 = secret_block.get()

    generic_client = RsClient(
        rs_server_href,
        rs_server_api_key=apikey1,
        owner_id=None,
        logger=None,
    )
    stac_client = generic_client.get_catalog_client()
    a_collection = "S100_L0"
    stac_client.remove_collection(a_collection)
    # Define a search interval
    start_date = datetime(2010, 1, 1, 12, 0, 0)
    stop_date = datetime(2024, 1, 1, 12, 0, 0)
    response = stac_client.add_collection(
        Collection(
            id=a_collection,
            description=None,
            extent=Extent(
                spatial=SpatialExtent(bboxes=[-180.0, -90.0, 180.0, 90.0]),
                temporal=TemporalExtent([start_date, stop_date]),
            ),
        ),
    )
    response.raise_for_status()


@task
def step2():
    pass


@flow
def hello_world6():
    step1()
    step2()
