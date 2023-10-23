from django.core.management.base import BaseCommand
from scripts.mysql.db_settings import SQLManager
import mysql.connector

class Command(BaseCommand):
    help = 'Delete all rows data from specific tables'

    def handle(self, *args, **kwargs):
        tables = [
            'script_article_info',
            'script_title_img',
            'script_demographic_profile',
            'script_faqs',
            'script_outline_intro',
            'script_outline',
            'script_outline_conclusion',
            'script_outline_body',
            'script_content_introduction',
            'script_content_conclusion',
            'script_content_body',
            'script_images_body',
            'script_document',
            'script_blog_excerpts',
            'script_per_prompt_cost',
            'script_total_prompt_cost',
            'script_keywords'
        ]

        conn = SQLManager.connect_to_db()
        if conn is None:
            print("No database connection.")
            return

        try:
            c = conn.cursor()
            for table_name in tables:
                c.execute(f"DELETE FROM {table_name}")
                self.stdout.write(self.style.SUCCESS(f"All rows from table {table_name} were deleted successfully."))
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Database operation failed: {str(e)}")
        finally:
            conn.close()
