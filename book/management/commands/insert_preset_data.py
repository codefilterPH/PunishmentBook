from django.core.management.base import BaseCommand
from book.models import (
    PunishmentLibrary, OffenseLibrary, PlaceOfOmission, AFP_Personnel,
    ImposedByWhom
)
import datetime

class Command(BaseCommand):
    help = 'Preset data to the models'

    def insert_to_offense(self, text):
        try:
            print('Inserting data into the Offense Violation Library...')
            violation = OffenseLibrary(violation=text['offense'])
            violation.save()
            self.stdout.write(self.style.SUCCESS('Successfully inserted data into the Offense Violation Library.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))

    def insert_to_date_place_omission(self, params):
        try:
            print('Inserting data into the place of omission...')

            place = params['place_of_omission'][0]
            date = params['place_of_omission'][1]

            omission = PlaceOfOmission(place=place, date=date)
            omission.save()
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

    def insert_imposer(self, params):
        try:
            print('Inserting data into imposed by whom...')
            for item in params['imposed_by_whom']:
                print(f'RECEIVED IMPOSER: {item}')
                punishment = ImposedByWhom(name=item)
                punishment.save()

            self.stdout.write(self.style.SUCCESS('Successfully inserted data into the Punishment Library.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))

    def insert_to_afp_personnel(self, params):
        try:
            print('Inserting data into the AFP Personnel...')
            personnel = AFP_Personnel(
                afpsn=params['afpsn'],
                last_name=params['last'],
                first_name=params['first'],
                middle_name=params['middle'],
                rank_id=params['rank']
            )
            personnel.save()
            self.stdout.write(self.style.SUCCESS('Successfully inserted data into the AFP Personnel Record.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))

    @staticmethod
    def get_format_date():
        try:
            cur_date = datetime.datetime.now()
            # Format the current date and time as "YYYY-MM-DD HH:MM"
            formatted_datetime = cur_date.strftime('%Y-%m-%d %H:%M')
            print(f'\n\nFORMATTED DATE: {formatted_datetime}\n\n')
            return formatted_datetime
        except Exception as e:
            return f"Error: {e}"

    def handle(self, *args, **kwargs):

        data = {
            "offense": "Violation of R.A 7877 (Anti-Sexual Harassment Act of 1995) and R.A 11313 (Safe Spaces Act)",
            "place_of_omission": ["CJVAB, Pasay City", self.get_format_date()],
            "punishment": "Restriction within CJVAB and to certain specified limits without suspension from duty and/or any activities for sixty (60) consecutive days.",
            "imposed_by_whom": ["CO, PAFHRMC", "First Sergeant"],
            "rank": "AM",
            "afpsn": "987960",
            "last": "Bulahan",
            "first": "Eugene",
            "middle": "Lugatiman"
        }

        self.insert_to_punishment(data)
        self.insert_to_offense(data)
        self.insert_to_date_place_omission(data)
        self.insert_to_afp_personnel(data)
        self.insert_imposer(data)

