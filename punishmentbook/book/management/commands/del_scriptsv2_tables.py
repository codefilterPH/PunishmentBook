from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Deletes all tables for the scriptsv2 app'

    def handle(self, *args, **kwargs):
        # Getting all table names for the scriptsv2 app
        with connection.cursor() as cursor:
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name LIKE 'scriptsv2_%'")
            table_list = [row[0] for row in cursor.fetchall()]

        # Check if there are any tables to drop
        if not table_list:
            self.stdout.write(self.style.WARNING("No tables found for the scriptsv2 app."))
            return

        # Confirming the action from the user
        self.stdout.write(self.style.WARNING(f"Going to delete tables: {', '.join(table_list)}"))
        confirm = input("Are you sure you want to delete these tables? [yes/no]: ")
        if confirm.lower() != 'yes':
            self.stdout.write(self.style.ERROR("Aborted!"))
            return

        # Drop foreign key constraints
        with connection.cursor() as cursor:
            for table in table_list:
                cursor.execute("""SELECT CONSTRAINT_NAME 
                                  FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
                                  WHERE REFERENCED_TABLE_SCHEMA = DATABASE() 
                                  AND TABLE_NAME = %s;""", [table])
                fk_constraints = [row[0] for row in cursor.fetchall()]
                for constraint in fk_constraints:
                    cursor.execute(f"ALTER TABLE {table} DROP FOREIGN KEY {constraint};")

        # Dropping the tables
        with connection.cursor() as cursor:
            for table in table_list:
                cursor.execute(f"DROP TABLE {table};")

        self.stdout.write(self.style.SUCCESS("All scriptsv2 tables have been deleted."))
