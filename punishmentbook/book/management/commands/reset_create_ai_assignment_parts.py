from django.core.management.base import BaseCommand
from scriptsv2.models import ArtificialIntelligenceList, AiModelVariations, AIPrimaryAssignment
from content.models import ContentType

class Command(BaseCommand):
    help = 'Reset > Delete > Create default AI and Variations'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.default_variation = None

    def handle(self, *args, **kwargs):
        # Populate AI and their variations
        self.populate_ai_and_variations()
        # Set default AI model variation
        self.set_default_variation()
        # Populate AI Primary Assignments
        self.populate_ai_primary_assignments()
        # Update or create assignments
        self.create_or_update_assignments()

        self.stdout.write(self.style.SUCCESS('All tasks completed successfully!'))

    def populate_ai_and_variations(self):

        data = [
            {
                "label": "Poe",
                "variations": [
                    {"variation": "Assistant", "value": "capybara"},
                    {"variation": "Claude-instant-100k", "value": "a2_100k"},
                    {"variation": "Claude-2-100k", "value": "a2_2"},
                    {"variation": "Claude-instant", "value": "a2"},
                    {"variation": "ChatGPT", "value": "chinchilla"},
                    {"variation": "ChatGPT-16k", "value": "agouti"},
                    {"variation": "GPT-4", "value": "beaver"},
                    {"variation": "GPT-4-32k", "value": "vizcacha"},
                    {"variation": "Google-PaLM", "value": "acouchy"},
                    {"variation": "Llama-2-7b", "value": "llama_2_7b_chat"},
                    {"variation": "Llama-2-13b", "value": "llama_2_13b_chat"},
                    {"variation": "Llama-2-70b", "value": "llama_2_70b_chat"},
                    {"variation": "Vicuna-13B-V13", "value": "vicuna13bv13"}
                ]
            },
            {
                "label": "ChatGPT",
                "variations": [
                    {"variation": "Gpt 4", "value": "gpt-4"},
                    {"variation": "Gpt3.5 Turbo", "value": "gpt-3.5-turbo"},
                    {"variation": "Gpt3.5 Turbo 16k", "value": "gpt-3.5-turbo-16k"},
                    {"variation": "Gpt 4 0613", "value": "gpt-4-0613"},
                    {"variation": "Text Davinci 2", "value": "text-davinci-002"},
                    {"variation": "Text Davinci 3", "value": "text-davinci-003"},
                ]
            },
            {
                "label": "Bard",
                "variations": [
                    {"variation": "Bard", "value": "bard"},
                ]
            },
            {
                "label": "Claude",
                "variations": [
                    {"variation": "Claude", "value": "claude"},
                ]
            },
            {
                "label": "Bedrock",
                "variations": [
                    {"variation": "Amazon Titan Large", "value": "amazon.titan-tg1-large"},
                    {"variation": "Amazon Titan Medium", "value": "amazon.titan-e1t-medium"},
                    {"variation": "Ai21 Jurrasic Mid", "value": "ai21.j2-mid"},
                    {"variation": "Ai21 Jurrasic Ultra", "value": "ai21.j2-ultra"},
                    {"variation": "Claude Instant", "value": "anthropic.claude-instant-v1"},
                    {"variation": "Claude V1", "value": "anthropic.claude-v1"},
                    {"variation": "Claude V2", "value": "anthropic.claude-v2"},
                ]
            }
        ]

        for ai_data in data:
            ai, created = ArtificialIntelligenceList.objects.get_or_create(label=ai_data['label'])
            for var in ai_data['variations']:
                defaults = {
                    "variation": var['variation'],
                    "value": var['value'],
                    "is_default": var.get('is_default', False)
                }
                AiModelVariations.objects.update_or_create(ai=ai, variation=var['variation'], defaults=defaults)

        self.stdout.write(self.style.SUCCESS('AI Models and Variations populated successfully!'))

    def set_default_variation(self):

        # Check if any variation has is_default set to True
        default_variation_exists = AiModelVariations.objects.filter(is_default=True).exists()

        # If no default is found, set ChatGPT's "Gpt 4 0613" variation as default
        if not default_variation_exists:
            chatgpt = ArtificialIntelligenceList.objects.get(label="ChatGPT")
            gpt4_0613_variation, created = AiModelVariations.objects.get_or_create(
                ai=chatgpt,
                variation="Gpt 4 0613",
                defaults={"value": "gpt-4-0613", "is_default": True}
            )
            if not created:
                gpt4_0613_variation.is_default = True
                gpt4_0613_variation.save()

        self.default_variation = AiModelVariations.objects.filter(is_default=True).first()
        if not self.default_variation:
            self.stdout.write(self.style.ERROR('No default AI Model Variation found!'))
            return

    def populate_ai_primary_assignments(self):
        AIPrimaryAssignment.objects.all().delete()
        default_parts = [
            "Target Niche",
            "Purpose",
            "Customer Avatar",
            "Type Of Persons",
            "Serp Analysis",
            "Title",
            "Meta Description",
            "Faq",
            "Outline",
            "Introduction",
            "Body",
            "Conclusion",
            "Readability",
            "Avoid AI Detection",
            "Italic and Bold",
            "Breaking Paragraph",
            "Stats",
            "List",
            "Table",
            "Key Takeaways",
            "External Link",
            "Point Of View",
            "Enhance Fix",
            "Authoritative",
            "LSI and NLP"
        ]

        default_variation = AiModelVariations.objects.filter(is_default=True).first()
        default_content_type = ContentType.objects.filter(is_default=True).first()

        if default_variation and default_content_type:  # Ensure both are available
            for part in default_parts:
                AIPrimaryAssignment.objects.update_or_create(
                    content_part=part,
                    primary_ai=default_variation,
                    backup_ai=default_variation,
                    defaults={
                        "content_part": part,
                        "primary_ai": default_variation,
                        "backup_ai": default_variation,
                        "is_fixer": 0,
                        "category": "test",
                        "content_type": default_content_type
                    }
                )
        else:
            print("Error: Default AI Variation or Default Content Type not found!")
        self.stdout.write(self.style.SUCCESS('AI Primary Assignments populated successfully!'))

    @staticmethod
    def create_or_update_assignments():
        data = [
            {
                'content_part': 'Key Takeaways',
                'primary_ai': {'ai': 'Poe', 'variation': 'Llama', 'value': 'llama_2_70b_chat'},
                'backup_ai': {'ai': 'Bard', 'variation': 'bard', 'value': 'bard'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 1
            },
            {
                'content_part': 'Key Takeaways',
                'primary_ai': {'ai': 'Poe', 'variation': 'Llama-2-70b', 'value': 'llama_2_70b_chat'},
                'backup_ai': {'ai': 'Bard', 'variation': 'bard', 'value': 'bard'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 1
            },
            {
                'content_part': 'Table',
                'primary_ai': {'ai': 'Poe', 'variation': 'Llama-2-70b', 'value': 'llama_2_70b_chat'},
                'backup_ai': {'ai': 'Bard', 'variation': 'bard', 'value': 'bard'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 1
            },
            {
                'content_part': 'Table',
                'primary_ai': {'ai': 'Poe', 'variation': 'Llama-2-70b', 'value': 'llama_2_70b_chat'},
                'backup_ai': {'ai': 'Bard', 'variation': 'bard', 'value': 'bard'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 1
            },
            {
                'content_part': 'List',
                'primary_ai': {'ai': 'Poe', 'variation': 'Llama-2-70b', 'value': 'llama_2_70b_chat'},
                'backup_ai': {'ai': 'Bard', 'variation': 'bard', 'value': 'bard'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 1
            },
            {
                'content_part': 'List',
                'primary_ai': {'ai': 'Poe', 'variation': 'Llama-2-70b', 'value': 'llama_2_70b_chat'},
                'backup_ai': {'ai': 'Bard', 'variation': 'bard', 'value': 'bard'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 1
            },
            {
                'content_part': 'Stats',
                'primary_ai': {'ai': 'Poe', 'variation': 'Llama-2-70b', 'value': 'llama_2_70b_chat'},
                'backup_ai': {'ai': 'Bard', 'variation': 'bard', 'value': 'bard'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 1
            },
            {
                'content_part': 'Stats',
                'primary_ai': {'ai': 'Poe', 'variation': 'Llama-2-70b', 'value': 'llama_2_70b_chat'},
                'backup_ai': {'ai': 'Bard', 'variation': 'bard', 'value': 'bard'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 1
            },
            {
                'content_part': 'Breaking Paragraph',
                'primary_ai': {'ai': 'Poe', 'variation': 'Llama-2-70b', 'value': 'llama_2_70b_chat'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 1
            },
            {
                'content_part': 'Breaking Paragraph',
                'primary_ai': {'ai': 'Poe', 'variation': 'Llama-2-70b', 'value': 'llama_2_70b_chat'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 1
            },
            {
                'content_part': 'Italic and Bold',
                'primary_ai': {'ai': 'Poe', 'variation': 'Llama-2-70b', 'value': 'llama_2_70b_chat'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 1
            },
            {
                'content_part': 'Italic and Bold',
                'primary_ai': {'ai': 'Poe', 'variation': 'Llama-2-70b', 'value': 'llama_2_70b_chat'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 1
            },
            {
                'content_part': 'Avoid AI Detection',
                'primary_ai': {'ai': 'Poe', 'variation': 'Llama-2-70b', 'value': 'llama_2_70b_chat'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 1
            },
            {
                'content_part': 'Avoid AI Detection',
                'primary_ai': {'ai': 'Poe', 'variation': 'Llama-2-70b', 'value': 'llama_2_70b_chat'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 1
            },
            {
                'content_part': 'Readability',
                'primary_ai': {'ai': 'Poe', 'variation': 'Llama-2-70b', 'value': 'llama_2_70b_chat'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 1
            },
            {
                'content_part': 'Readability',
                'primary_ai': {'ai': 'Poe', 'variation': 'Llama-2-70b', 'value': 'llama_2_70b_chat'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 1
            },
            {
                'content_part': 'Target Niche',
                'primary_ai': {'ai': 'Poe', 'variation': 'Llama-2-70b', 'value': 'llama_2_70b_chat'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Target Niche',
                'primary_ai': {'ai': 'Poe', 'variation': 'Llama-2-70b', 'value': 'llama_2_70b_chat'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'prd',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Purpose',
                'primary_ai': {'ai': 'Bard', 'variation': 'Bard', 'value': 'bard'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Purpose',
                'primary_ai': {'ai': 'Bard', 'variation': 'Bard', 'value': 'bard'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Customer Avatar',
                'primary_ai': {'ai': 'Bard', 'variation': 'Bard', 'value': 'bard'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt3.5 Turbo 16k', 'value': 'gpt-3.5-turbo-16k'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Customer Avatar',
                'primary_ai': {'ai': 'Bard', 'variation': 'Bard', 'value': 'bard'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt3.5 Turbo 16k', 'value': 'gpt-3.5-turbo-16k'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Type Of Persons',
                'primary_ai': {'ai': 'Poe', 'variation': 'Llama-2-70b', 'value': 'llama_2_70b_chat'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Type Of Persons',
                'primary_ai': {'ai': 'Poe', 'variation': 'Llama-2-70b', 'value': 'llama_2_70b_chat'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Serp Analysis',
                'primary_ai': {'ai': 'Bard', 'variation': 'Bard', 'value': 'bard'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt3.5 Turbo 16k', 'value': 'gpt-3.5-turbo-16k'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Serp Analysis',
                'primary_ai': {'ai': 'Bard', 'variation': 'Bard', 'value': 'bard'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt3.5 Turbo 16k', 'value': 'gpt-3.5-turbo-16k'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Title',
                'primary_ai': {'ai': 'Claude', 'variation': 'Claude', 'value': 'claude'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Title',
                'primary_ai': {'ai': 'Claude', 'variation': 'Claude', 'value': 'claude'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Meta Description',
                'primary_ai': {'ai': 'Bard', 'variation': 'Bard', 'value': 'bard'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Meta Description',
                'primary_ai': {'ai': 'Bard', 'variation': 'Bard', 'value': 'bard'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Outline',
                'primary_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Outline',
                'primary_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Faq',
                'primary_ai': {'ai': 'ChatGPT', 'variation': 'Gpt3.5 Turbo 16k', 'value': 'gpt-3.5-turbo-16k'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt3.5 Turbo', 'value': 'gpt-3.5-turbo'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Faq',
                'primary_ai': {'ai': 'ChatGPT', 'variation': 'Gpt3.5 Turbo 16k', 'value': 'gpt-3.5-turbo-16k'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt3.5 Turbo', 'value': 'gpt-3.5-turbo'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Introduction',
                'primary_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Introduction',
                'primary_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Body',
                'primary_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Body',
                'primary_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Conclusion',
                'primary_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'Conclusion',
                'primary_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 0
            },
            {
                'content_part': 'LSI and NLP',
                'primary_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 1
            },
            {
                'content_part': 'LSI and NLP',
                'primary_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 1
            },
            {
                'content_part': 'External Link',
                'primary_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'test',
                'content_type': 'authoritative',
                'is_fixer': 1
            },
            {
                'content_part': 'External Link',
                'primary_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'backup_ai': {'ai': 'ChatGPT', 'variation': 'Gpt 4 0613', 'value': 'gpt-4-0613'},
                'category': 'prod',
                'content_type': 'authoritative',
                'is_fixer': 1
            }
        ]
        for entry in data:
            # Check existence
            obj, created = AIPrimaryAssignment.objects.update_or_create(
                content_part=entry['content_part'],
                category=entry['category'],
                defaults={
                    'primary_ai': AiModelVariations.objects.get(value=entry['primary_ai']['value']),
                    'backup_ai': AiModelVariations.objects.get(value=entry['backup_ai']['value']),
                    'content_type': ContentType.objects.get_or_create(content_type=entry['content_type'].lower())[0],
                    'is_fixer': entry['is_fixer']
                }
            )

            if created:
                print(f"Created new entry for content_part: {entry['content_part']} in category: {entry['category']}")
            else:
                print(f"Updated entry for content_part: {entry['content_part']} in category: {entry['category']}")
