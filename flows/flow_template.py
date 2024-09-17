from prefect import flow, task
from utils.artifacts import ReportManager

report_manager = ReportManager(4)


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
def flow_template() -> str:
    step1().submit
    step2().submit
    step3().submit
    step4().submit
    report_manager.add_report_as_artefact("flow-template-test", "Template" )
    return "This is a flow template"


if __name__ == "__main__":
    flow_template() 
    
    