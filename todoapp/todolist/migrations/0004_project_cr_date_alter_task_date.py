# Generated by Django 5.1.4 on 2025-02-18 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0003_task_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='cr_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
