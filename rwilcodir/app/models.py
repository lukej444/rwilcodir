from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class Employee(AbstractUser):
    employee_id = models.IntegerField(unique=True)
    supervisor = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='employees')
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='employee_set', related_query_name='employee')
    user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), blank=True, related_name='employee_set', related_query_name='employee')
    username = models.CharField(_('username'), max_length=150, unique=True, default='default_username')
    password = models.CharField(_('password'), max_length=128, default='default_password')
    is_supervisor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Training(models.Model):
    name = models.CharField(max_length=100)
    training_id = models.IntegerField()
    description = models.TextField(default='')

    def __str__(self):
        return self.name

class TrainingStatus(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    completion_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    def __str__(self):
        return str(self.employee) + " - " + str(self.training)

    def completion_percentage(self):
        total_trainings = TrainingStatus.objects.filter(employee=self.employee).count()
        completed_trainings = TrainingStatus.objects.filter(employee=self.employee, completion_date__isnull=False).count()
        if total_trainings > 0:
            return int(completed_trainings / total_trainings * 100)
        else:
            return 0
