from django.core.management.base import BaseCommand
from book.models import PunishmentLibrary, OffenseLibrary

class Command(BaseCommand):
    help = 'Preset data to the models'

    def insert_to_offense(self, text):
        try:
            print('Inserting data into the Offense Violation Library...')
            violation = OffenseLibrary(violation=text)
            violation.save()
            self.stdout.write(self.style.SUCCESS('Successfully inserted data into the Offense Violation Library.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))

    def insert_to_punishment(self, text):
        try:
            print('Inserting data into the Punishment Library...')
            punishment = PunishmentLibrary(punishment=text)
            punishment.save()
            self.stdout.write(self.style.SUCCESS('Successfully inserted data into the Punishment Library.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))

    def handle(self, *args, **kwargs):
        offense = "Violation of R.A 7877 (Anti-Sexual Harassment Act of 1995) and R.A 11313 (Safe Spaces Act)"
        punishment = "Restriction within CJVAB and to certain specified limits without suspension from duty and/or any activities for sixty (60) consecutive days."  # The data you want to insert

        self.insert_to_punishment(punishment)
        self.insert_to_offense(offense)