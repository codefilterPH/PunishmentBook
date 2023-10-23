from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import glob

class Command(BaseCommand):
    help = 'Deletes all migrations for the app'

    def handle(self, *args, **options):
        for app in settings.INSTALLED_APPS:
            # Ignore Django's built-in apps, we're interested in user-defined apps only
            if "django" not in app:
                # Path to the migrations directory
                migrations_dir = os.path.join(app, 'migrations')
                if os.path.exists(migrations_dir):
                    # Find all Python files in the migrations directory (excluding __init__.py)
                    migration_files = glob.glob(os.path.join(migrations_dir, '[!__init__]*.py'))

                    # Delete each migration file
                    for file in migration_files:
                        os.remove(file)

                    self.stdout.write(self.style.SUCCESS(f'Successfully deleted migrations for {app}'))

        self.stdout.write(self.style.SUCCESS('Successfully deleted all migrations'))
