from prefect import flow
from prefect.artifacts import create_markdown_artifact

@task
def generate_report():
    report = "# Rapport de flux\n test Hello World"
    return report

@flow
def my_flow() -> str:
    report = generate_report()
    create_markdown_artifact(key="rapport", markdown=report)
    return "Hello, world!"
