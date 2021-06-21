from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

import cx_Oracle
from core.database.models import Teacher


class Command(BaseCommand):
    help = 'Create Database Schema.'

    def handle(self, *args, **kwargs):
        teacher = Teacher()
        sql = f"select id from quizapp_teachers where user_id = 15"
        teacher_id = teacher.execute_select_sql(sql)[0]['id']
        print(teacher_id)

        # for r in res:
        #     print(r)