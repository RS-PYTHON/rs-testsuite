from prefect import flow, task
from prefect.events import emit_event
from datetime import datetime, timedelta
from flows.utils.artifacts import ReportManager
import time

report_manager = ReportManager(2)


@task(name="station-connection", description="Connect to the station")
def connect():
    report_manager.success_step(1, "Connect to station")
    time.sleep(1)

@task(name="get-session", description="Retrieve the list of sessions between two dates")
def retrieve_session(to, tf):
    report_manager.success_step(2, f"Retrieve sessions between {to} and {tf}")
    time.sleep(2)

@task
def send_events():
    send_event(3, "MTI", "S1A_20241114143038056332")
    send_event(4, "MPS", "S1A_20251314143031111111")
    send_event(5, "MTI", "S1A_20231144143348056552")


def send_event(step, station, session_id):
    event_json = {
        "mission": "s1",
        "level": "raw",
        "station": f"{station}",
        "session_id": f"{session_id}"
    }
    emit_event(event="new.session.event", resource=event_json)
    report_manager.success_step(step, f"Send event for session {session_id}")


@flow
def retrieve_s1_list_of_sessions(delta_time_seconds: int):
    now = datetime.now()
    before = now - timedelta(seconds=delta_time_seconds)

    markdown_report = f"""## Summary

This flow will retrieve sentinel-1 sessions from stations between two dates :
- **Start date**: {before.strftime("%Y-%m-%d %H:%M:%S")}
- **End date**: {now.strftime("%Y-%m-%d %H:%M:%S")}

"""
    report_manager.add_markdown_as_artefact("summary", markdown_report, "")

    # Start the 2 tasks in sequence
    connect()
    retrieve_session(before, now)
    send_events()

    report_manager.add_report_as_artefact("retrieve-sentinel1-sessions", "retrieve sentinel-1 sessions")


if __name__ == "__main__":
    retrieve_s1_list_of_sessions()
