from django.core.management.base import BaseCommand
from scriptsv2.models import EncapsulateToHtmlTag

class Command(BaseCommand):
    help = 'Insert initial data for EncapsulateToHtmlTag'

    def handle(self, *args, **options):
        if not EncapsulateToHtmlTag.objects.exists():
            EncapsulateToHtmlTag.objects.create(encap=True)
            self.stdout.write(self.style.SUCCESS('Successfully inserted initial data for EncapsulateToHtmlTag'))
        else:
            self.stdout.write(self.style.WARNING('Data for EncapsulateToHtmlTag already exists. No data inserted.'))
