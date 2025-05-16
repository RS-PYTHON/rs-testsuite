from prefect import flow, task
from datetime import datetime, timedelta
from flows.utils.artifacts import ReportManager

report_manager = ReportManager(2)


@task(name="station-connection", description="Connect to the station")
def connect():
    report_manager.success_step(1, "Connect to station")

@task(name="get-session", description="Retrieve the list of sessions between two dates")
def retrieve_session(to, tf):
    report_manager.success_step(2, f"Retrieve sessions between {to} and {tf}")

@flow
def retrieve_s1_list_of_sessions(delta_time_seconds: int) -> str:
    now = datetime.now()
    before = now - timedelta(seconds=delta_time_seconds)

    markdown_report = f"""# Sales Report
## Summary

This flow will retrieve sentinel-1 sessions from stations between two dates :
- **Start date**: {before.strftime("%Y-%m-%d %H:%M:%S")}
- **End date**: {now.strftime("%Y-%m-%d %H:%M:%S")}

"""
    report_manager.add_markdown_as_artefact("summary", markdown_report, "my description")

    # Start the 2 tasks in sequence
    connect()
    retrieve_session(before, now)

    report_manager.add_report_as_artefact("retrieve-sentinel1-sessions", "Template")
    return "This is a flow template"


if __name__ == "__main__":
    retrieve_s1_list_of_sessions()
