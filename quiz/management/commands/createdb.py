from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

import cx_Oracle
from core.database.schema import schemaCreation


class Command(BaseCommand):
    help = 'Create Database Schema.'

    def handle(self, *args, **kwargs):
        if settings.CUSTOM_DB_CONFIG:
            
            try:
                connection = cx_Oracle.connect(
                    user=settings.CUSTOM_DB_CONFIG['user'],
                    password=settings.CUSTOM_DB_CONFIG['password'],
                    dsn=settings.CUSTOM_DB_CONFIG['dsn']
                )
                print("Database connention has successfully.")

                schemaCreation()

            except cx_Oracle.Error as err:
                print(err)
                print("Couldn't connect the database.")
        else:
            print("""
                Database Configuration not found in settings file.
                example:
                CUSTOM_DB_CONFIG = {
                    'user': '<username>',
                    'password': '<password>',
                    'dsn': '<dsn string>'
                }
            """)