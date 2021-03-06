# Generated by Django 3.0.5 on 2021-06-21 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_auto_20210621_0640'),
        ('quiz', '0006_auto_20210621_0711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='marks',
            field=models.IntegerField(),
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.IntegerField(blank=True)),
                ('question', models.ManyToManyField(blank=True, to='quiz.Question')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Course')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Teacher')),
            ],
        ),
    ]
