from django.db import models
from django.contrib.auth.models import User
import random, string

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    plan_type = models.CharField(max_length=8, default="Home")
    
class Guest(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Guest: {self.code}"



