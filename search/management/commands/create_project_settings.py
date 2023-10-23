from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.db import connections, DatabaseError, DEFAULT_DB_ALIAS

sql_script = """
    ALTER TABLE content_project
    ADD COLUMN add_readability INT DEFAULT 1,
    ADD COLUMN add_stats INT DEFAULT 1,
    ADD COLUMN add_bold_italic INT DEFAULT 1,
    ADD COLUMN add_list INT DEFAULT 1,
    ADD COLUMN add_external_link INT DEFAULT 1,
    ADD COLUMN add_table INT DEFAULT 1,
    ADD COLUMN add_faqs INT DEFAULT 1,
    ADD COLUMN add_schema INT DEFAULT 1,
    ADD COLUMN content_type VARCHAR(255) DEFAULT 'authoritative',
    ADD COLUMN add_lsi_keywords INT DEFAULT 1,
    ADD COLUMN lsi_keywords JSON,
    ADD COLUMN break_up_paragraphs INT DEFAULT 1,
    ADD COLUMN add_key_takeways INT DEFAULT 1,
    ADD COLUMN add_image INT DEFAULT 1,
    ADD COLUMN point_of_view VARCHAR(255) DEFAULT 'second person',
    ADD COLUMN readability VARCHAR(255) DEFAULT '7th Grader',
    ADD COLUMN avoid_ai_detection INT DEFAULT 1,
    ADD COLUMN add_video INT DEFAULT 1,
    ADD COLUMN article_length INT DEFAULT 3500,
    ADD COLUMN auto_length INT DEFAULT 0;
"""
sql_script_keyword = """
    ALTER TABLE content_keyword
    ADD COLUMN add_readability INT DEFAULT 1,
    ADD COLUMN add_stats INT DEFAULT 1,
    ADD COLUMN add_bold_italic INT DEFAULT 1,
    ADD COLUMN add_list INT DEFAULT 1,
    ADD COLUMN add_external_link INT DEFAULT 1,
    ADD COLUMN add_table INT DEFAULT 1,
    ADD COLUMN add_faqs INT DEFAULT 1,
    ADD COLUMN add_schema INT DEFAULT 1,
    ADD COLUMN content_type VARCHAR(255) DEFAULT 'authoritative',
    ADD COLUMN add_lsi_keywords INT DEFAULT 1,
    ADD COLUMN lsi_keywords JSON,
    ADD COLUMN break_up_paragraphs INT DEFAULT 1,
    ADD COLUMN add_key_takeways INT DEFAULT 1,
    ADD COLUMN add_image INT DEFAULT 1,
    ADD COLUMN point_of_view VARCHAR(255) DEFAULT 'second person',
    ADD COLUMN avoid_ai_detection INT DEFAULT 1,
    ADD COLUMN add_video INT DEFAULT 1,
    ADD COLUMN type_of_person VARCHAR(255);
"""

sql_script_content_type = """
CREATE TABLE content_contenttype (
    id SERIAL PRIMARY KEY,
    content_type VARCHAR(255) DEFAULT 'authoritative'
);
"""
sql_check_empty_table = """
    SELECT COUNT(*) FROM content_contenttype;
"""
sql_script_insert_content_type = """
    INSERT INTO content_contenttype (content_type)
    VALUES
        ('authoritative'),
        ('case studies'),
        ('how To''s'),
        ('guides'),
        ('listicles'),
        ('local pages'),
        ('local service pages'),
        ('service pages'),
        ('category pages for shopify ecom stores'),
        ('data driven content'),
        ('news style articles'),
        ('press releases');
"""

sql_script_pov = """
    CREATE TABLE content_pointofview (
        id SERIAL PRIMARY KEY,
        point_of_view VARCHAR(255) DEFAULT 'second person'
    );
"""
sql_check_pov_empty_table = """
    SELECT COUNT(*) FROM content_pointofview;
"""
sql_script_insert_pov = """
    INSERT INTO content_pointofview (point_of_view)
    VALUES
        ('first person'),
        ('second person'),
        ('third person');
"""

sql_script_create_typesofpersons = """
    CREATE TABLE content_typesofpersons (
        id SERIAL PRIMARY KEY,
        keyword_id INTEGER REFERENCES content_keyword(id) ON DELETE CASCADE,
        type_of_person_array JSON
);
"""
class Command(BaseCommand):
    help = 'If ContentCraft DB does not exist, create it. Then run makemigrations and migrate.'

    def handle(self, *args, **options):
        # Check if database exists
        db_conn = connections[DEFAULT_DB_ALIAS]
        try:
            with db_conn.cursor() as cursor:
                cursor.execute(sql_script)
                print("SQL script PROJECT executed successfully.")
        except Exception as e:
            print("Error executing SQL script PROJECT:", e)
        try:
            with db_conn.cursor() as cursor:
                cursor.execute(sql_script_keyword)
                print("SQL script KEYWORD executed successfully.")
        except Exception as e:
            print("Error executing SQL script KEYWORD:", e)
        try:
            with db_conn.cursor() as cursor:
                cursor.execute(sql_script_content_type)
                print("SQL script CONTENT TYPE executed successfully.")
        except Exception as e:
            print("Error executing SQL script CONTENT TYPE:", e)
        try:
            with db_conn.cursor() as cursor:
                cursor.execute(sql_script_pov)
                print("SQL script POV executed successfully.")
        except Exception as e:
            print("Error executing POV SQL script:", e)
        try:
            with db_conn.cursor() as cursor:
                cursor.execute(sql_check_empty_table)
                row_count = cursor.fetchone()[0]

            if row_count == 0:
                with db_conn.cursor() as cursor:
                    cursor.execute(sql_script_insert_content_type)
                    print("Data inserted into CONTENT TYPE table.")
            else:
                print("Table already has CONTENT TYPE data. Skipping insertion.")
        except Exception as e:
            print("Error executing SQL SCRIPT:", e)
        try:
            with db_conn.cursor() as cursor:
                cursor.execute(sql_check_pov_empty_table)
                row_count = cursor.fetchone()[0]

            if row_count == 0:
                with db_conn.cursor() as cursor:
                    cursor.execute(sql_script_insert_pov)
                    print("Data inserted into POV table.")
            else:
                print("Table already has POV data. Skipping insertion.")
        except Exception as e:
            print("Error executing SQL SCRIPT:", e)
        try:
            with db_conn.cursor() as cursor:
                cursor.execute(sql_script_create_typesofpersons)
                print("SQL script Types of Persons executed Successfully")
        except Exception as e:
            print(f"Error in executing Types of Persons SQL Script: {str(e)}")

