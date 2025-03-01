from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.core import validators

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    cr_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'


class Task(models.Model):
    Choices = [(1, 'high'),
               (2, 'medium'),
               (3, 'low'),
               (4, 'nop')]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, unique=True)
    title = models.CharField(max_length=200, validators=[validators.MinLengthValidator(5, message='Your title is too short')])
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    is_completed = models.BooleanField(default=False, verbose_name="Is Completed")
    priority = models.SmallIntegerField(choices=Choices, default=4)
    deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

        constraints = (models.CheckConstraint(condition=Q(priority__lte=4), name='priority_condition'),)