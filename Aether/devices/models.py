from django.db import models
from users.models import Owner


class House(models.Model):
    owner = models.ForeignKey(Owner, related_name='houses', on_delete=models.CASCADE)
    house_id = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return f"House #{self.house_id} owned by {self.owner.user.first_name}"

class Room(models.Model):
    house = models.ForeignKey('House', related_name='rooms', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    room_id = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return f"{self.name} in House #{self.house.house_id}"


class Device(models.Model):
    device_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    general_product_code = models.CharField(max_length=100)  # unique product code for model
    manufacturer = models.CharField(max_length=200, blank=True)
    average_energy_consumption_per_hour = models.FloatField(default=10)  # default value if not present in JSON
    status = models.CharField(max_length=50, choices=[('on', 'On'), ('off', 'Off'), ('idle', 'Idle'), ('error', 'Error')], default='off')
    room = models.ForeignKey(Room, related_name='devices', on_delete=models.CASCADE)
    device_number = models.PositiveIntegerField(default=1)  # To distinguish same model devices within a room

    def __str__(self):
        return f"{self.name} ({self.device_number}) in {self.room.name}"

