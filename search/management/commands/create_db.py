# your_app/management/commands/create_db.py

import MySQLdb
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = 'Creates the db if it does not exist - For Development only'

    def add_arguments(self, parser):
        parser.add_argument(
            '-d', '--database',
            type=str,
            help='Name of the database to create',
            default=None
        )

    def handle(self, *args, **options):
        # Use the provided database name or ask for one
        if options['database']:
            database_name = options['database']
        else:
            database_name = input("Please enter the name of the database to create: ")

        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        host = settings.DATABASES['default']['HOST']

        db = MySQLdb.connect(user=user, passwd=password, host=host)
        cursor = db.cursor()

        try:
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {database_name};')
            db.commit()
            self.stdout.write(self.style.SUCCESS(f'Database {database_name} created successfully (or already exists)'))
        except MySQLdb.Error as e:
            db.rollback()
            self.stdout.write(self.style.ERROR(f'An error occurred while creating the database: {e}'))
        finally:
            cursor.close()
            db.close()

        try:
            # Make migrations and then migrate
            call_command('makemigrations')
            call_command('migrate', '--noinput')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred while running migrations: {e}'))
