from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import connection

class Command(BaseCommand):
    help = 'Check and create missing columns for specified app model'

    def handle(self, *args, **kwargs):
        app_name = input("App name: ")
        table_name = input("Table or Class Name: ")

        try:
            # Fetch the model
            model = apps.get_model(app_label=app_name, model_name=table_name)

            # Introspect the database table
            with connection.cursor() as cursor:
                table_description = connection.introspection.get_table_description(cursor, model._meta.db_table)
                db_columns = {column.name for column in table_description}

            # Fetch fields from the model excluding relations
            model_fields = {field.column for field in model._meta.fields if not field.is_relation}

            # Determine missing fields
            missing_fields = model_fields - db_columns

            if missing_fields:
                print(f"Missing columns: {', '.join(missing_fields)}")
                # Add missing columns
                for field_name in missing_fields:
                    field = model._meta.get_field(field_name)
                    with connection.schema_editor() as editor:
                        editor.add_field(model, field)
                    print(f"Successfully added column '{field_name}' to '{model._meta.db_table}' table.")
            else:
                print("All columns are in sync!")

        except Exception as e:
            print(f"Error: {e}")

