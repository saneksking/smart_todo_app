# Generated by Django 4.2.7 on 2024-01-25 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0004_task_time_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='time_end',
            field=models.DateField(),
        ),
    ]
