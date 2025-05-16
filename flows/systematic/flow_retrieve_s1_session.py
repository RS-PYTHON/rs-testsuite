from prefect import flow, task
from flows.utils.artifacts import ReportManager

report_manager = ReportManager(2)


@task(name="station-connection", description="Connect to the station")
def connect():
    report_manager.success_step(1, "Step1 description")

@task(name="get-session", description="Retrieve the list of sessions between two dates")
def retrieve_session():
    report_manager.success_step(2, "Step2 description")

@flow
def retrieve_s1_list_of_sessions() -> str:
    markdown_report = """# Sales Report

## Summary

In the past quarter, our company saw a significant increase in sales, with a total revenue of $1,000,000. 
This represents a 20% increase over the same period last year.

## Sales by Region

| Region        | Revenue |
|:--------------|-------:|
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
    report_manager.add_markdown_as_artefact("summary", markdown_report, "my description")

    # Start the 2 tasks in sequence
    connect()
    retrieve_session()

    report_manager.add_report_as_artefact("retrieve-sentinel1-sessions", "Template")
    return "This is a flow template"


if __name__ == "__main__":
    retrieve_s1_list_of_sessions()
