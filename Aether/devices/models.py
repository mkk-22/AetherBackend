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
        return f"{self.name} Room in House #{self.house.house_id}"

class Device(models.Model):
    name = models.CharField(max_length=255)
    device_id = models.CharField(max_length=255, unique=True)
    general_product_code = models.CharField(max_length=255)
    average_energy_consumption_per_hour = models.DecimalField(max_digits=5, decimal_places=2)
    room = models.ForeignKey(Room, related_name='devices', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, 
        choices=[('on', 'On'), ('off', 'Off'), ('idle', 'Idle'), ('error', 'Error')]
    )

    def __str__(self):
        return f"Device #{self.device_id} in {self.room.name} Room, Status: {self.status}"