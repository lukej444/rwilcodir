# Generated by Django 4.1.7 on 2023-04-23 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_employee_options_alter_employee_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='is_supervisor',
            field=models.BooleanField(default=False),
        ),
    ]
