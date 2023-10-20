# your_app/management/commands/delete_db.py

import MySQLdb
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Deletes the db if it exists - For Development only'

    def handle(self, *args, **options):
        # Prompt for the database name
        database_name = input("Please enter the name of the database to delete: ")

        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        host = settings.DATABASES['default']['HOST']

        db = MySQLdb.connect(user=user, passwd=password, host=host)
        cursor = db.cursor()

        try:
            cursor.execute(f'DROP DATABASE IF EXISTS {database_name};')
            db.commit()
            self.stdout.write(self.style.SUCCESS(f'Database {database_name} deleted successfully (or did not exist)'))
        except MySQLdb.Error as e:
            db.rollback()
            self.stdout.write(self.style.ERROR(f'An error occurred while deleting the database: {e}'))
        finally:
            cursor.close()
            db.close()
