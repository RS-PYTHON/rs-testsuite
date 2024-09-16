from prefect import flow, task
from utils.artifacts import ReportManager


report_manager = ReportManager()

@task
def step1():
    report_manager.success_step(1, "Step1 description")

@task
def step2():
    report_manager.success_step(2, "Step2 description")

@task
def step3():
    report_manager.failed_step(3, "Step3 description")

@task
def step4():
    report_manager.success_step(4, "Step4 description")
    
    
@flow
def my_flow5() -> str:
    step1()
    step2()
    step3()
    step4()
    report_manager.add_report_as_artefact("Hello World test", "Template" )
    return "Hello, world!"

if __name__ == "__main__":
    my_flow5() 
    
    