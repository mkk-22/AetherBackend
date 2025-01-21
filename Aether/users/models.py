from django.db import models
from django.contrib.auth.models import User

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    plan_type = models.CharField(max_length=8, default="Home")
    house_id = models.BigIntegerField(default=0)
    
class Guest(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=20, unique=True)
    house_id = models.BigIntegerField(default=0)
    
    def __str__(self):
        return f"Guest: {self.user.first_name}"
