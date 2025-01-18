from django.db import models
from django.contrib.auth.models import User
from devices.models import House
from energy.models import EnergyGoal

class HomeOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    house = models.OneToOneField(House, on_delete=models.CASCADE)
    PLAN_CHOICES = (
        ("HOME", "home"),
        ("BUSINESS", "business")
    )
    plan_type = models.CharField(choices=PLAN_CHOICES, max_length=8)
    energy_goal = models.OneToOneField(EnergyGoal, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
 

class Guest(models.Model):
    host = models.ForeignKey(HomeOwner, on_delete=models.CASCADE, related_name='guests')
    name = models.CharField(max_length=255)
    guest_code = models.CharField(max_length=255, unique=True)
    allowed_rooms = models.ManyToManyField('devices.Room')
    
    def __str__(self):
        return f"{self.name} ({self.guest_code})"


    
