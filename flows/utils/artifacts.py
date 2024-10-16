from prefect.artifacts import create_table_artifact
# wait for v3 - from prefect.artifacts import create_progress_artifact, update_progress_artifact
from datetime import datetime


class ReportManager:
    def __init__(self, number_steps: int):
        self.number_steps = number_steps
        self.report = []
        """
            wait for v3
            self.progress_artifact_id = create_progress_artifact(
            progress=0.0,
            description="Test progress...",
            )
        """

    def success_step(self, step: int, description: str):
        item = {
            'step': step,
            'description': f'{description}',
            'status': 'OK',
        }
        self.report.append(item)

    def failed_step(self, step: int, description: str):
        item = {
            'step': step,
            'description': f'{description}',
            'status': 'NOK',
        }
        self.report.append(item)

    def add_report_as_artefact(self, key_value, description_value):
        # Artifact key must only contain lowercase letters, numbers, and dashes. (type=value_error)
        now = datetime.now()

        # Formater la date et l'heure en texte
        date_texte = now.strftime("%A %d %B %Y, %H:%M:%S")

        return create_table_artifact(
            key=key_value.lower(),
            table=self.report,
            description=description_value + " - " + date_texte
        )
