from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.core import validators
from django.utils.timezone import now
from datetime import timedelta

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

    def time_remaining(self):
        """Возвращает timedelta, если дедлайн установлен, иначе None."""
        if self.deadline:
            return self.deadline - now()
        return None

    def time_remaining_dict(self):
        remaining = self.time_remaining()  # Получаем timedelta
        if remaining is None:
            return None

        total_seconds = int(remaining.total_seconds())
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        return {"days": days, "hours": hours, "minutes": minutes, "seconds": seconds}

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

        constraints = (models.CheckConstraint(condition=Q(priority__lte=4), name='priority_condition'),)