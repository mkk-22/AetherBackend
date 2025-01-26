from django.db import models
from devices.models import Room, Device


class AmbianceMode(models.Model):
    room = models.ForeignKey(Room, related_name='modes', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Name of the mode (e.g., "Movie Night", "Relaxation")

    def __str__(self):
        return f"{self.name} mode for {self.room.name}"


class AmbianceModeDevice(models.Model):
    mode = models.ForeignKey(AmbianceMode, related_name='devices', on_delete=models.CASCADE)
    device = models.ForeignKey(Device, related_name='controlled_by_modes', on_delete=models.CASCADE)
    light_color = models.CharField(max_length=100, blank=True, null=True)  # Optional (e.g., "blue", "red")
    volume = models.PositiveIntegerField(blank=True, null=True)  # Optional, for speaker control
    temperature = models.FloatField(default='24.0')
    status = models.CharField(max_length=50, choices=[('on', 'On'), ('off', 'Off')], default='on')  # Turn on/off

    def __str__(self):
        return f"{self.device.name} in {self.mode.name} mode"
