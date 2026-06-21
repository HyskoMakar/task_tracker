from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'Not done'),
        ('PROGRESS', 'Progress'),
        ('DONE', 'Complete')
    ]
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High')
    ]

    title = models.CharField(max_length=64)
    description = models.TextField()
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='TODO')
    priority = models.CharField(max_length=8, choices=PRIORITY_CHOICES, default='MEDIUM')
    due_day = models.DateTimeField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title