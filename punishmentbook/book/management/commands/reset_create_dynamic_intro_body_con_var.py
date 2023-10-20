from django.core.management.base import BaseCommand
from scriptsv2.models import MultilineVariableExtractor, AIPrimaryAssignment, VariableValuePair

DATA = {
    'Introduction': {
        'general_tone': "Conversational tone of voice that's casual, yet professional - warm and welcoming.",
        'target_niche': "",
        'purpose': '',
        'customer_avatar': '',
        'keyword': '',
        'title': '',
        'search_intent': "Informational",
        'language': "English",
        'outline_temp': '',
        'point_of_view': "Second Persons",
    },
    'Body': {
        'general_tone': "Conversational tone of voice that's casual, yet professional - warm and welcoming.",
        'target_niche': '',
        'purpose': '',
        'customer_avatar': '',
        'keyword': '',
        'title': '',
        'search_intent': "Informational",
        'language': "English",
        'outline_temp': '',
        'point_of_view': "Second Person",
    },
    'Conclusion': {
        'general_tone': "Conversational tone of voice that's casual, yet professional - warm and welcoming.",
        'point_of_view': "Second Person",
        'target_niche': '',
        'purpose': '',
        'customer_avatar': '',
        'keyword': '',
        'title': '',
        'search_intent': "Informational",
        'language': "English",
        'outline_temp': ''
    }
}

class Command(BaseCommand):
    help = 'Reset > Delete > Create default variables.'

    def handle(self, *args, **options):
        MultilineVariableExtractor.objects.all().delete()
        VariableValuePair.objects.all().delete()

        for content_part, variable_data in DATA.items():
            ai_primary_instance, created = AIPrimaryAssignment.objects.get_or_create(content_part=content_part)
            multiline_extractor = MultilineVariableExtractor.objects.create(content_parts=ai_primary_instance)

            for variable_name, variable_value in variable_data.items():
                VariableValuePair.objects.create(
                    extractor=multiline_extractor,
                    variable_name=variable_name,
                    variable_value=variable_value
                )

            self.stdout.write(self.style.SUCCESS(f'Successfully inserted data for content part "{content_part}"'))