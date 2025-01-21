from django.db import models
from django.contrib.auth.models import User 
from users.models import Owner


class EnergyGoal(models.Model):
    homeowner = models.OneToOneField(Owner, on_delete=models.CASCADE, related_name='energy_goal')
    goal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.homeowner.username}'s Energy Goal: {self.goal} kWh"

class EnergyUsage(models.Model):
    homeowner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='energy_usages')
    creation_timestamp = models.DateTimeField()
    total_consumption = models.DecimalField(max_digits=10, decimal_places=2) 
    period = models.CharField(max_length=10, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')])

    def __str__(self):
        return f"{self.homeowner.username}'s {self.period.capitalize()} Energy Usage: {self.total_consumption} kWh"


class IntervalReading(models.Model):
    device_id = models.CharField(max_length=255)
    homeowner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interval_readings')
    start = models.DateTimeField()
    end = models.DateTimeField()
    usage = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return f"Reading for Device {self.device_id} from {self.start_time} to {self.end_time} - {self.usage} kWh"
