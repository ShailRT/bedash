from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('super', 'Superuser'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='employee')
    

class Todo(models.Model):
    TASK_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    task = models.CharField(max_length=255)
    user_assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_to")
    user_assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="assigned_by")
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.task

class Team(models.Model):
    managers = models.ManyToManyField(User, related_name="manager")
    members = models.ManyToManyField(User, related_name="members")
