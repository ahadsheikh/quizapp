# Generated by Django 3.0.5 on 2021-06-21 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_auto_20210621_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.IntegerField(choices=[(1, 'Option1'), (1, 'Option2'), (3, 'Option3'), (4, 'Option4')]),
        ),
    ]