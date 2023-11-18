from django.core.management.base import BaseCommand
from book.models import OffenseLibrary
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Inserts article of war list into OffenseLibrary model'

    def handle(self, *args, **options):
        data = [
            {"abbreviations": "AW", "article_number": 24, "violation": "Right of an accused under investigation"},
            {"abbreviations": "AW", "article_number": 54, "violation": "Fraudulent Enlistment"},
            {"abbreviations": "AW", "article_number": 55, "violation": "Officers making unlawful enlistment"},
            {"abbreviations": "AW", "article_number": 56, "violation": "False musters"},
            {"abbreviations": "AW", "article_number": 57, "violation": "False return – omissions to render returns"},
            {"abbreviations": "AW", "article_number": 58, "violation": "Certain acts to constitute desertion"},
            {"abbreviations": "AW", "article_number": 59, "violation": "Desertion"},
            {"abbreviations": "AW", "article_number": 60, "violation": "Advising or aiding another to desert"},
            {"abbreviations": "AW", "article_number": 61, "violation": "Entertaining a deserter"},
            {"abbreviations": "AW", "article_number": 62, "violation": "Absence without Leave (AWOL)"},
            {"abbreviations": "AW", "article_number": 63, "violation": "Disrespect toward the Pres, VP, Congress of the Phil, or SND"},
            {"abbreviations": "AW", "article_number": 64, "violation": "Disrespect towards Superior Officer"},
            {"abbreviations": "AW", "article_number": 65, "violation": "Assaulting or willfully disobeying superior officer"},
            {"abbreviations": "AW", "article_number": 66, "violation": "Insubordinate conduct towards NCO"},
            {"abbreviations": "AW", "article_number": 67, "violation": "Mutiny or sedition"},
            {"abbreviations": "AW", "article_number": 68, "violation": "Failure to suppress mutiny or sedition"},
            {"abbreviations": "AW", "article_number": 69, "violation": "Quarrels, frays and disorder"},
            {"abbreviations": "AW", "article_number": 70, "violation": "Arrest or confinement"},
            {"abbreviations": "AW", "article_number": 71, "violation": "Charges Action Upon"},
            {"abbreviations": "AW", "article_number": 72, "violation": "Refusal to receive or keep prisoners"},
            {"abbreviations": "AW", "article_number": 73, "violation": "Report of prisoners received"},
            {"abbreviations": "AW", "article_number": 74, "violation": "Releasing prisoner without proper authority"},
            {"abbreviations": "AW", "article_number": 75, "violation": "Delivery of offenders to Civil Authorities"},
            {"abbreviations": "AW", "article_number": 76, "violation": "Misbehavior before the enemy"},
            {"abbreviations": "AW", "article_number": 77, "violation": "Subordinates compelling Commanders to surrender"},
            {"abbreviations": "AW", "article_number": 78, "violation": "Improper use of countersign"},
            {"abbreviations": "AW", "article_number": 79, "violation": "Forcing a safeguard"},
            {"abbreviations": "AW", "article_number": 80, "violation": "Captured property to be secured for public service"},
            {"abbreviations": "AW", "article_number": 81, "violation": "Dealing in captured or abandoned property"},
            {"abbreviations": "AW", "article_number": 82, "violation": "Relieving, corresponding with or aiding the enemy"},
            {"abbreviations": "AW", "article_number": 83, "violation": "Spies"},
            {"abbreviations": "AW", "article_number": 84, "violation": "Willful or negligent loss, damage or wrong disposition of mil property"},
            {"abbreviations": "AW", "article_number": 85, "violation": "Waste or unlawful disposition of Military property"},
            {"abbreviations": "AW", "article_number": 86, "violation": "Dunk on duty"},
            {"abbreviations": "AW", "article_number": 87, "violation": "Misbehavior of sentinel"},
            {"abbreviations": "AW", "article_number": 88, "violation": "Personal interest in the sale of provisions"},
            {"abbreviations": "AW", "article_number": 89, "violation": "Intimidation of persons bringing provisions"},
            {"abbreviations": "AW", "article_number": 90, "violation": "Good order to be maintained and wrong redressed"},
            {"abbreviations": "AW", "article_number": 91, "violation": "Provoking speeches or gesture"},
            {"abbreviations": "AW", "article_number": 92, "violation": "Dueling"},
            {"abbreviations": "AW", "article_number": 93, "violation": "Military personnel who commit rape or murder"},
            {"abbreviations": "AW", "article_number": 94, "violation": "Various Crimes"},
            {"abbreviations": "AW", "article_number": 95, "violation": "Frauds against the government"},
            {"abbreviations": "AW", "article_number": 96, "violation": "Conduct unbecoming of an officer and gentleman"},
            {"abbreviations": "AW", "article_number": 97, "violation": "GENERAL ARTICLE"},
            {"abbreviations": "AW", "article_number": 98, "violation": "When an by Whom ordered"},
            {"abbreviations": "AW", "article_number": 99, "violation": "Composition"},
            {"abbreviations": "AW", "article_number": 100, "violation": "Challenges"},
            {"abbreviations": "AW", "article_number": 101, "violation": "Oath of Members and Recorders"},
            {"abbreviations": "AW", "article_number": 102, "violation": "Power Procedures"},
            {"abbreviations": "AW", "article_number": 103, "violation": "Opinion of Merits on Case"},
            {"abbreviations": "AW", "article_number": 104, "violation": "Record of Proceedings"},
            {"abbreviations": "AW", "article_number": 105, "violation": "Disciplinary action taken by the Commander"}
        ]

        try:
            # Create instances of OffenseLibrary with the provided data
            for entry in data:
                offense_instance = OffenseLibrary.objects.create(**entry)

            # Display a success message
            self.stdout.write(self.style.SUCCESS('Successfully inserted data for OffenseLibrary'))

        except IntegrityError as e:
            # Handle integrity error (e.g., unique constraint violation)
            self.stderr.write(self.style.ERROR(f'IntegrityError: {e}'))
            self.stderr.write(self.style.ERROR('Data insertion failed. Ensure uniqueness constraints are met.'))

        except Exception as e:
            # Handle other exceptions
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))
            self.stderr.write(self.style.ERROR('Data insertion failed. Check the provided data and try again.'))
