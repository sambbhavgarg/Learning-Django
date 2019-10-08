from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Banner(models.Model):
    Input = models.TextField(default = 'Whats on your mind')
    Date_Posted = models.DateTimeField(default=timezone.now())
    Author = models.ForeignKey(User, default='Anonymous', on_delete=models.CASCADE)
