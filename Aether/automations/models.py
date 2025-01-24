from django.db import models
from devices.models import Device

class Automation(models.Model):
    TRIGGER_TYPES = [
        ('time', 'Time'),
        ('temperature', 'Temperature'),
        ('humidity', 'Humidity'),
    ]

    name = models.CharField(max_length=255)
    trigger_type = models.CharField(max_length=50, choices=TRIGGER_TYPES)
    trigger_value = models.CharField(max_length=100)
    devices = models.ManyToManyField(Device, related_name='automations')

    def __str__(self):
        return f"Automation: {self.name} ({self.trigger_type}: {self.trigger_value})"


