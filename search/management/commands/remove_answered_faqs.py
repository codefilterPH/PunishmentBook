from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Removes the answered_faqs field from the ContentCraft table.'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            try:
                cursor.execute("ALTER TABLE content_contentcraft DROP COLUMN answered_faqs;")
                self.stdout.write(self.style.SUCCESS('Successfully removed the answered_faqs column from ContentCraft.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error occurred: {e}"))
