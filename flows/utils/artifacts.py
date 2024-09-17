from prefect.artifacts import create_table_artifact, create_markdown_artifact
# wait for v3 - from prefect.artifacts import create_progress_artifact, update_progress_artifact
from datetime import datetime

class ReportManager:
    def __init__(self, number_steps:int):
        self.number_steps = number_steps
        self.report = []
        """
            wait for v3
            self.progress_artifact_id = create_progress_artifact(
            progress=0.0,
            description="Test progress...",
            )
        """

    def success_step(self, step:int, description:str):
        item = {
            'step' : step,
            'description' : f'{description}',
            'status' : 'OK',            
        }
        self.report.append ( item )
        #self.__progress(step)

    def failed_step(self, step:int, description:str):
        item = {
            'step' : step,
            'description' : f'{description}',
            'status' : 'NOK',            
        }
        self.report.append ( item )
        #self.__progress(step)


    #def __progress(self, step:int):
    #    update_progress_artifact(self.progress_artifact_id, step / self.number_steps)
        

    def add_report_as_artefact(self, key_value, description_value):                
        # Artifact key must only contain lowercase letters, numbers, and dashes. (type=value_error)

        now = datetime.now()

        # Formater la date et l'heure en texte
        date_texte = now.strftime("%A %d %B %Y, %H:%M:%S")

        na_revenue = 500000
        markdown_report = f"""# Sales Report

        ## Summary

        In the past quarter, our company saw a significant increase in sales, with a total revenue of $1,000,000. 
        This represents a 20% increase over the same period last year.

        ## Sales by Region

        | Region        | Revenue |
        |:--------------|-------:|
        | North America | ${na_revenue:,} |
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
        create_markdown_artifact(
                key=key_value.lower(),
                markdown=markdown_report,
                description="Quarterly Sales Report",
        )


        return create_table_artifact(
            key=key_value.lower(),
            table=self.report,
            description= description_value + " - " + date_texte
        )
