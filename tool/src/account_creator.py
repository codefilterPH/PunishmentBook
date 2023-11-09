# import sys
#
# # Print all directories where Python is looking for modules
# project_path = '/home/paf_admin/dj_app/hrmis'
# sys.path.append(project_path)
#
# # for path in sys.path:
# #     print(path)
#
# import os
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrmis.settings')
# import django
#
# django.setup()
#
# # import mysql.connector
# import psycopg2
# from dotenv import load_dotenv
# # IMPORTS FOR INSERT FUNCTION
# from django.db import transaction
# from django.contrib.auth.models import User, Group
# from django.db.utils import IntegrityError
# from newsoidata.models import AfpPersonnelInfo
# from django.core.exceptions import ObjectDoesNotExist
#
# manage_py_dir = os.path.dirname(os.path.abspath(__file__))
# manage_py_dir = os.path.normpath(os.path.join(manage_py_dir, os.pardir, os.pardir))
# env_file_path = os.path.join(manage_py_dir, 'secrets', '.env')
# print(env_file_path)
# # Load environment variables from .env file
# load_dotenv(dotenv_path=str(env_file_path))
#
#
# class AccountCreator:
#     def __init__(self, serial):
#         # self.db_params = {
#         #     "host": 'localhost',
#         #     "database": 'hrmisdj_db',
#         #     "user": 'postgres',
#         #     "password": 'Adm1nP@ssC@rd2020',
#         # }
#
#         self.db_params = {
#             "host": os.getenv('DB_HOST', 'localhost'),
#             "database": os.getenv('DB_NAME', 'hrmisdj_db'),
#             "user": os.getenv('DB_USER', 'postgres'),
#             "password": os.getenv('DB_PASSWORD', 'Adm1nP@ssC@rd2020'),
#         }
#
#         self.personnel_id = 0
#         self.first_name = ''
#         self.middle_name = ''
#         self.last_name = ''
#         self.afpsn = serial
#
#         print(f'VERSION 2')
#         print(self.db_params['host'])
#         print(self.db_params['database'])
#         print(self.db_params['user'])
#         print(self.db_params['password'])
#
#     def check_afp_personnel(self):
#         """Check personnel if it did exist in afp personnel"""
#         try:
#             # Connect to the PostgreSQL database
#             connection = psycopg2.connect(
#                 host=self.db_params["host"],
#                 database=self.db_params["database"],
#                 user=self.db_params["user"],
#                 password=self.db_params["password"]
#             )
#             cursor = connection.cursor()
#
#             # Query to check if the AFP serial number exists in the afp_personnel table
#             query = "SELECT id, first_name, middle_name, last_name FROM afp_personnel WHERE afpsn = %s"
#             cursor.execute(query, (self.afpsn,))
#             result = cursor.fetchone()
#
#             print(f"Executing query for AFP Serial Number: {self.afpsn}")
#
#             if result:
#                 self.personnel_id = result[0]
#                 self.first_name = result[1]
#                 self.middle_name = result[2]
#                 self.last_name = result[3]
#                 # print(f"AFP Serial Number '{self.afpsn}' exists in afp_personnel table.")
#                 # print(f"First Name: {self.first_name}")
#                 # print(f"Middle Name: {self.middle_name}")
#                 # print(f"Last Name: {self.last_name}")
#
#             else:
#                 print(f"AFP Serial Number '{self.afpsn}' does not exist in AFP PERSONNEL table.")
#                 return False
#
#             cursor.close()
#             connection.close()
#             return True
#         except psycopg2.Error as e:
#             print(f"Error: {e}")
#             return False
#
#     def verify_id_to_auth_user(self):
#         """Check personnel if it did exist in auth user model"""
#         try:
#             if self.personnel_id is not None:
#                 django.setup()
#                 # Query the user with the provided personnel_id
#                 user = User.objects.filter(id=self.personnel_id).first()
#
#                 if user:
#                     # The user exists in the 'auth_user' table
#                     print(
#                         f'Personnel {user.first_name}-{user.username} with id of {self.personnel_id} already exists in AUTH USER! Skipping...')
#                     return True
#                 else:
#                     # The user does not exist in the 'auth_user' table
#                     print(f'Personnel with id of {self.personnel_id} does not exist yet! Creating an account...')
#                     return False
#             else:
#                 print("Personnel ID is None or not provided.")
#                 return False
#         except Exception as e:
#             print(f"Error: {e}")
#             return False
#
#     def insert_user_with_group(self):
#         """Directly insert the data to the table if not exists in auth user and auto add group."""
#         try:
#             if self.personnel_id:
#                 django.setup()
#                 with transaction.atomic():
#                     # Insert a new user into the 'auth_user' table
#                     user, created = User.objects.get_or_create(
#                         id=int(self.personnel_id),
#                         defaults={
#                             'password': "pbkdf2_sha256$260000$56EK2AWy0vgBQVBgsO8ljl$iSMkFBhnxZpDAXFXefRt5Gmp/hc1N3Hs59lH1xrX5j0=",
#                             'last_login': "2023-08-31 00:07:20.294838+00",
#                             'is_superuser': 'f',
#                             'username': str(self.afpsn),
#                             'first_name': str(self.first_name),
#                             'last_name': str(self.last_name),
#                             'email': "sample@example.com",
#                             'is_staff': 'f',
#                             'is_active': 't',
#                             'date_joined': "2023-08-31 06:56:51+00"
#                         }
#                     )
#
#                     if created:
#                         # If the user was created, insert the user into the 'auth_user_groups' table
#                         user_group = Group.objects.get(id=1)
#                         user.groups.add(user_group)
#                         print("User and group created successfully!")
#                     else:
#                         print("User already exists, no action taken.")
#
#                     print('UPDATING MARITAL STATUS AND DATE OF BIRTH OF BIRTH')
#
#                     # Check if the record with pers_id '887969' exists
#                     if AfpPersonnelInfo.objects.filter(pers_id='887969').exists():
#                         try:
#                             # Perform the update if the record exists
#                             AfpPersonnelInfo.objects.filter(pers_id='887969').update(marital_stat='SINGLE',
#                                                                                      birth_date='1900-01-01')
#                             print("Record updated successfully.")
#                         except Exception as e:
#                             # Handle any other exceptions that may occur
#                             print(f"An error occurred while updating the record: {e}")
#                     else:
#                         # If the record does not exist, do nothing or handle accordingly
#                         print("No record found with pers_id '887969'. No update performed.")
#
#             else:
#                 print("Personnel ID is 0 or None!")
#
#         except IntegrityError as e:
#             print(f"Error: {e}")
#             print("Rolling back the transaction...")
#             transaction.set_rollback(True)
#         except Exception as e:
#             print(f"Error: {e}")
#             print("Rolling back the transaction...")
#             transaction.set_rollback(True)
#
#     def reset_user_password(self):
#         try:
#             # Try to get the user by username
#             user = User.objects.get(username=self.afpsn)
#
#             # Set the new password
#             user.set_password(
#                 "pbkdf2_sha256$260000$56EK2AWy0vgBQVBgsO8ljl$iSMkFBhnxZpDAXFXefRt5Gmp/hc1N3Hs59lH1xrX5j0=")
#             user.save()
#
#             print(f"Password for user '{self.afpsn}' has been reset successfully.")
#
#         except ObjectDoesNotExist:
#             # If the user does not exist, print an error message
#             print(f"User '{self.afpsn}' does not exist.")
#         except Exception as e:
#             # Catch any other exceptions and print an error message
#             print(f"An error occurred: {e}")
#
#     def run_all(self):
#         afp_personnel_acct = self.check_afp_personnel()
#         auth_user_acct = self.verify_id_to_auth_user()
#         print(f'PERSONNEL EXISTS: {afp_personnel_acct}')
#         print(f'AUTH USER NOT EXISTS: {auth_user_acct}')
#
#         if afp_personnel_acct and auth_user_acct:
#             print('BOTH ALREADY EXISTS MIGHT FORGOT THE PASSWORD')
#             # self.reset_user_password()
#         elif afp_personnel_acct and not auth_user_acct:
#             print('PERSONNEL EXISTS BUT NO AUTH USER. PROCEED INSERTION OF AUTH USER ACCOUNT')
#         # self.insert_user_with_group()
#         else:
#             print('Personnel not exists in afp_personnel. Please create first in hrmis7.')
#
#
# if __name__ == "__main__":
#     # Database connection parameters
#     # pip install python-dotenv
#
#     afpsn = input("Enter the AFP Serial Number: ")
#     afp_verifier = AccountCreator(afpsn)
#     afp_verifier.run_all()
#     # afp_verifier.reset_user_password()
