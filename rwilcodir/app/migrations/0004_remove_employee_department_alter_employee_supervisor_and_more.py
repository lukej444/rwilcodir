# Generated by Django 4.1.7 on 2023-04-22 21:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_department_alter_employee_supervisor_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='department',
        ),
        migrations.AlterField(
            model_name='employee',
            name='supervisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='trainingstatus',
            name='completion_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.DeleteModel(
            name='Department',
        ),
    ]
