from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import connection

class Command(BaseCommand):
    help = 'Check models and create missing tables and fields'

    def handle(self, *args, **options):
        # Get list of tables that already exist in the database
        existing_tables = connection.introspection.table_names()

        for model in apps.get_models():
            table_name = model._meta.db_table
            # Check if table exists
            if table_name not in existing_tables:
                self.stdout.write(self.style.SUCCESS(f'Table for model {model} does not exist.'))
                self.stdout.write('Please run `python manage.py migrate` to create the table.')
                continue

            # If table exists, check for fields
            db_fields = [field[0] for field in connection.introspection.get_table_description(connection.cursor(), table_name)]
            model_fields = [field.column for field in model._meta.fields]

            for field in model_fields:
                if field not in db_fields:
                    self.stdout.write(self.style.WARNING(f"Field {field} in model {model} doesn't exist in the database."))
                    self.stdout.write('Please run `python manage.py makemigrations` followed by `python manage.py migrate` to create the missing fields.')

        self.stdout.write(self.style.SUCCESS('Finished checking models.'))

