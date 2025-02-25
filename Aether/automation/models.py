from django.db import models
from devices.models import Device

class Automation(models.Model):
    name = models.CharField(max_length=255)
    trigger_time = models.TimeField()
    devices_on = models.ManyToManyField(Device, related_name='automations_on') 
    devices_off = models.ManyToManyField(Device, related_name='automations_off') 

    def __str__(self):
        return f"Automation: {self.name} (Trigger Time: {self.trigger_time})"