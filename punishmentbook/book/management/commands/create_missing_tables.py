from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import connection


class Command(BaseCommand):
    help = 'Create missing database tables for all models in a specified app'

    def add_arguments(self, parser):
        parser.add_argument('app_name', help='Name of the Django app containing the models')

    def handle(self, *args, **kwargs):
        app_name = kwargs['app_name']

        try:
            # Get all models for the specified app
            app = apps.get_app_config(app_name)
            models = list(app.get_models())

            with connection.cursor() as cursor:
                # Get a list of existing table names
                existing_tables = connection.introspection.table_names()

                MAX_RETRIES = 3
                retry_count = 0

                while models and retry_count < MAX_RETRIES:
                    failed_models = []

                    for model in models:
                        table_name = model._meta.db_table

                        # Check if the table already exists
                        if table_name not in existing_tables:
                            try:
                                # Create the table
                                with connection.schema_editor() as schema_editor:
                                    schema_editor.create_model(model)
                                self.stdout.write(self.style.SUCCESS(f"Table '{table_name}' created successfully."))
                            except Exception as inner_e:
                                failed_models.append(model)
                                self.stdout.write(self.style.ERROR(f"Failed to create table '{table_name}': {inner_e}"))
                        else:
                            self.stdout.write(self.style.SUCCESS(f"Table '{table_name}' already exists."))

                    models = failed_models
                    retry_count += 1

                if models:  # if there are still models left
                    self.stdout.write(self.style.ERROR("Some tables couldn't be created after retries."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
