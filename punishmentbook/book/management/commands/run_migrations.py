from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.db import connections, DatabaseError, DEFAULT_DB_ALIAS

class Command(BaseCommand):
    help = 'If ContentCraft DB does not exist, create it. Then run makemigrations and migrate.'

    def handle(self, *args, **options):
        # Check if database exists
        db_conn = connections[DEFAULT_DB_ALIAS]
        try:
            db_conn.cursor()
        except DatabaseError:
            self.stderr.write(self.style.ERROR(f'Database "{db_conn.settings_dict["NAME"]}" does not exist. Please create it manually.'))
            return

        # If database exists, run makemigrations and migrate
        try:
            call_command('makemigrations')
            call_command('migrate')
            self.stdout.write(self.style.SUCCESS('Successfully ran makemigrations and migrate.'))
        except CommandError as e:
            self.stderr.write(self.style.ERROR(str(e)))
