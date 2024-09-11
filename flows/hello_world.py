from prefect import flow, task
from prefect.artifacts import create_markdown_artifact

@task
def generate_report() -> str:
    report = "# Rapport de flux\n test Hello World \n yes "
    report += "AAAA \n "
    report += "BBB \n "
    return report

@flow
def my_flow5() -> str:
    create_markdown_artifact(key="rapport5", markdown=generate_report())
    return "Hello, world!"

if __name__ == "__main__":
    my_flow5() 
    
    