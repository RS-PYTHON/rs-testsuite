# Copyright 2023-2026 Airbus
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# wait for v3 - from prefect.artifacts import create_progress_artifact, update_progress_artifact
from datetime import datetime

from prefect.artifacts import create_table_artifact


class ReportManager:
    """_summary_"""

    def __init__(self, number_steps: int):
        self.number_steps = number_steps
        self.report: list[dict] = []
        """
            wait for v3
            self.progress_artifact_id = create_progress_artifact(
            progress=0.0,
            description="Test progress...",
            )
        """

    def success_step(self, step: int, description: str):
        item = {
            "step": step,
            "description": f"{description}",
            "status": "OK",
        }
        self.report.append(item)

    def failed_step(self, step: int, description: str):
        item = {
            "step": step,
            "description": f"{description}",
            "status": "NOK",
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
            description=description_value + " - " + date_texte,
        )
