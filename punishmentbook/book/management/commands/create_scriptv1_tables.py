from django.core.management.base import BaseCommand
import MySQLdb
from django.conf import settings
class Command(BaseCommand):
    help = 'Create database tables'

    def handle(self, *args, **kwargs):
        database_name = input("Please enter the name of the database to use/create: ")

        # Connect to MySQL
        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        host = settings.DATABASES['default']['HOST']

        db = MySQLdb.connect(user=user, passwd=password, host=host, db=database_name)
        cursor = db.cursor()

        tables_and_columns = [
            ('script_article_info', {'id': 'INT AUTO_INCREMENT PRIMARY KEY', 'title': 'TEXT', 'meta_description': 'TEXT', 'project': 'TEXT', 'user': 'INT', 'keyw_id': 'INT'}),
            ('script_title_img', {'id': 'INT AUTO_INCREMENT PRIMARY KEY', 'title': 'TEXT', 'img': 'TEXT', 'project': 'TEXT', 'user': 'INT', 'keyw_id': 'INT'}),
            ('script_demographic_profile', {'id': 'INT AUTO_INCREMENT PRIMARY KEY', 'demographic': 'TEXT', 'project': 'TEXT', 'user': 'INT', 'keyw_id': 'INT'}),
            ('script_faqs', {'id': 'INT AUTO_INCREMENT PRIMARY KEY', 'questions': 'TEXT', 'project': 'TEXT', 'user': 'INT', 'keyw_id': 'INT'}),
            ('script_outline_intro', {'id': 'INT AUTO_INCREMENT PRIMARY KEY', 'position': 'INT', 'header': 'TEXT', 'outline': 'TEXT', 'subsequent': 'TEXT', 'project': 'TEXT', 'user': 'INT', 'keyw_id': 'INT'}),
            ('script_outline', {'id': 'INT AUTO_INCREMENT PRIMARY KEY', 'outline_data': 'TEXT', 'project': 'TEXT', 'user': 'INT', 'keyw_id': 'INT'}),
            ('script_outline_conclusion', {'id': 'INT AUTO_INCREMENT PRIMARY KEY', 'position': 'INT', 'header': 'TEXT', 'outline': 'TEXT', 'subsequent': 'TEXT', 'project': 'TEXT', 'user': 'INT', 'keyw_id': 'INT'}),
            ('script_outline_body', {'id': 'INT AUTO_INCREMENT PRIMARY KEY', 'position': 'INT', 'header': 'TEXT', 'outline': 'TEXT', 'subsequent': 'TEXT', 'project': 'TEXT', 'user': 'INT', 'keyw_id': 'INT'}),
            ('script_content_introduction', {'id': 'INT AUTO_INCREMENT PRIMARY KEY', 'position': 'INT', 'content': 'TEXT', 'project': 'TEXT', 'user': 'INT', 'keyw_id': 'INT'}),
            ('script_content_conclusion', {'id': 'INT AUTO_INCREMENT PRIMARY KEY', 'position': 'INT', 'content': 'TEXT', 'project': 'TEXT', 'user': 'INT', 'keyw_id': 'INT'}),
            ('script_content_body', {'id': 'INT AUTO_INCREMENT PRIMARY KEY', 'position': 'INT', 'content': 'TEXT', 'project': 'TEXT', 'user': 'INT', 'keyw_id': 'INT'}),
            ('script_images_body', {'position': 'INT', 'header': 'TEXT', 'cur_img': 'TEXT', 'img1': 'TEXT', 'img2': 'TEXT', 'img3': 'TEXT', 'img4': 'TEXT', 'content_part': 'TEXT', 'project': 'TEXT', 'user': 'INT', 'keyw_id': 'INT'}),
            ('script_document', {'id': 'INT AUTO_INCREMENT PRIMARY KEY', 'article': 'TEXT', 'file_id': 'TEXT', 'url': 'TEXT'}),
            ('script_blog_excerpts', {'id': 'INT AUTO_INCREMENT PRIMARY KEY', 'excerpts': 'TEXT', 'project': 'TEXT', 'user': 'INT', 'keyw_id': 'INT'}),
            ('script_per_prompt_cost', {'id': 'INT AUTO_INCREMENT PRIMARY KEY', 'group_prompt_id': 'INT', 'tasks': 'TEXT', 'model': 'TEXT', 'cost': 'DECIMAL(10,5)', 'api_key': 'TEXT', 'timestamp': 'TEXT'}),
            ('script_total_prompt_cost', {'id': 'INT AUTO_INCREMENT PRIMARY KEY', 'project': 'TEXT', 'user': 'INT', 'keyword': 'INT', 'content': 'TEXT', 'total': 'DECIMAL(10,5)', 'api_key': 'TEXT', 'timestamp': 'TEXT'})
        ]

        for table_name, columns in tables_and_columns:
            self.create_db_and_table(cursor, table_name, columns)

        self.stdout.write(self.style.SUCCESS('All tables were created successfully.'))

    @staticmethod
    def create_db_and_table(cursor, table_name, columns):
        # Construct the SQL command
        columns_sql = ", ".join([f"{col_name} {col_type}" for col_name, col_type in columns.items()])
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});"

        # Execute the SQL command
        cursor.execute(create_table_sql)
