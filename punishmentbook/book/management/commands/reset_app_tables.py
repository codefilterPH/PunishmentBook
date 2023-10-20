from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Reset the database schema for a specific app'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='Name of the app to reset')

    def handle(self, *args, **options):
        app_name = options['app_name']

        # First, we'll unapply all migrations for the specified app
        self.stdout.write(self.style.WARNING(f'Rolling back all migrations for the app: {app_name}'))
        call_command('migrate', app_name, 'zero')

        # Then, we'll apply migrations again to recreate its schema
        self.stdout.write(self.style.WARNING(f'Migrating app: {app_name}'))
        call_command('migrate', app_name)

        self.stdout.write(self.style.SUCCESS(f'Successfully reset the database schema for the app: {app_name}'))
