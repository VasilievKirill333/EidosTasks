# Generated by Django 5.1.4 on 2025-02-16 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.SmallIntegerField(choices=[(1, 'high'), (2, 'medium'), (3, 'low'), (4, 'nop')], default=4),
        ),
    ]
