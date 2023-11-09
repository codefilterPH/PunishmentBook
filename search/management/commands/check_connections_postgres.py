from django.conf import settings
from django.core.management.base import BaseCommand
import psycopg2
import time

class CheckConnection:

    @staticmethod
    def connect_to_db():
        db_settings = settings.DATABASES['default']  # Gets the default database settings

        for attempt in range(3):
            try:
                conn = psycopg2.connect(
                    user=db_settings['USER'],
                    password=db_settings['PASSWORD'],
                    host=db_settings['HOST'],
                    port=db_settings.get('PORT', '5432'),
                    database=db_settings['NAME']
                )
                print(f"Connected to database: {db_settings['NAME']}")
                return conn
            except psycopg2.Error as e:
                print(f"Attempt {attempt + 1} to connect to database {db_settings['NAME']} failed: {str(e)}. Retrying in 5 seconds...")
                time.sleep(5)  # wait for 5 seconds before the next attempt

        raise psycopg2.Error(f"Failed to connect to database {db_settings['NAME']} after 3 attempts.")

class Command(BaseCommand):
    help = 'Checks the database connection'

    def handle(self, *args, **kwargs):
        try:
            CheckConnection.connect_to_db()
            self.stdout.write(self.style.SUCCESS('Successfully connected to the database!'))
        except psycopg2.Error as e:
            self.stderr.write(self.style.ERROR(f'Error connecting to the database: {str(e)}'))
