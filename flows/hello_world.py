from prefect import flow, task
from prefect.artifacts import create_markdown_artifact

@task
def generate_report():
    report = "# Rapport de flux\n test Hello World"
    return report

@flow
def my_flow() -> str:
    report = generate_report().result()  # Ajout de .result() pour obtenir le résultat de la tâche
    create_markdown_artifact(key="rapport", markdown=report)
    return "Hello, world!"

if __name__ == "__main__":
    my_flow()
