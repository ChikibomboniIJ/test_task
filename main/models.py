from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    STATUS_NEW = 'NEW'
    STATUS_IN_PROGRESS = 'IN PROGRESS'
    STATUS_COMPLETED = 'COMPLETED'

    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
    ]
    
    PRIORITY_LOW = 'LOW'
    PRIORITY_MEDIUM = 'MEDIUM'
    PRIORITY_HIGH = 'HIGH'
    
    PRIORITY_CHOICES  = [
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=255, 
                             verbose_name="Заголовок")
    
    desc = models.TextField(verbose_name="Описание")
    
    status = models.CharField(choices=STATUS_CHOICES,
                              default=STATUS_NEW,
                              max_length=11)
    
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=6)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name = "Создано")
    
    updated_at = models.DateTimeField(auto_now=True)