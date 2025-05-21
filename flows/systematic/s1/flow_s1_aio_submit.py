from prefect import flow, task, get_run_logger
from prefect.context import TaskRunContext
from flows.utils.artifacts import ReportManager
from prefect.deployments import run_deployment
from prefect.artifacts import create_markdown_artifact

# import json
# from prefect.deployments import run_deployment
import time

report_manager = ReportManager(2)


@task
def markdown_task():
    na_revenue = 500000
    markdown_report = f"""# Sales Report

## Summary

In the past quarter, our company saw a significant increase in sales, with a total revenue of $1,000,000. 
This represents a 20% increase over the same period last year.

## Sales by Region

| Region        | Revenue |
|:--------------|-------:|
| North America | ${na_revenue:,} |
| Europe        | $250,000 |
| Asia          | $150,000 |
| South America | $75,000 |
| Africa        | $25,000 |

## Top Products

1. Product A - $300,000 in revenue
2. Product B - $200,000 in revenue
3. Product C - $150,000 in revenue

## Conclusion

Overall, these results are very encouraging and demonstrate the success of our sales team in increasing revenue 
across all regions. However, we still have room for improvement and should focus on further increasing sales in 
the coming quarter.
"""
    create_markdown_artifact(
        key="gtm-report",
        markdown=markdown_report,
        description="Quarterly Sales Report",
    )


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
    markdown_task()
    s1_aio(station, session_id)


if __name__ == "__main__":
    s1_aio_submit("{}", "fake_session_name")