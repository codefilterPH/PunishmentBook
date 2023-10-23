# your_app_name/management/commands/create_script_total_prompt_cost_table.py

from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Creates the scriptsv2 script_total_prompt_cost table"

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE scriptsv2_scripttotalpromptcost (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    keyw_id INT,
                    content TEXT,
                    total DECIMAL(10,5),
                    api_key TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        self.stdout.write(self.style.SUCCESS('Successfully created table'))
