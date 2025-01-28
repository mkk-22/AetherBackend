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
    room_number = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.name} in House #{self.house.house_id}"


class Device(models.Model):
    room = models.ForeignKey(Room, related_name='devices', on_delete=models.CASCADE)
    device_id = models.CharField(max_length=100, primary_key=True)
    device_number = models.PositiveIntegerField(default=1)
    
    name = models.CharField(max_length=200)
    general_product_code = models.CharField(max_length=100)  
    manufacturer = models.CharField(max_length=200, blank=True)
    average_energy_consumption_per_hour = models.FloatField(default=10)  
    status = models.CharField(max_length=50, choices=[('on', 'On'), ('off', 'Off'), ('error', 'Error')], default='off')

    def __str__(self):
        return f"{self.name} ({self.device_number}) in {self.room.name}"

    def get_device_type(self):
        product_type = self.general_product_code[1]
        if product_type == 'T':  
            return 'Toggle'
        elif product_type == 'F':  
            return 'Fixed'
        elif product_type == 'V':  
            return 'Variable'
        elif product_type == 'M':  
            return 'Monitor'
        return 'Unknown'


class FixedOptionDevice(models.Model):
    device = models.ForeignKey(Device, related_name='fixed_device', on_delete=models.CASCADE)
    options = models.CharField(max_length=50, choices=[], default='')
    state = models.CharField(max_length=50, default='')

    def __str__(self):
        return f"Fixed Option Device => {self.device.name} (state: {self.state})"

class VariableOptionDevice(models.Model):
    device = models.ForeignKey(Device, related_name='variable_device', on_delete=models.CASCADE)
    state = models.IntegerField(default=25)  

    def __str__(self):
        return f"Variable Option Device => {self.device.name} (state: {self.state})"


class MonitorDevice(models.Model):
    device = models.ForeignKey(Device, related_name='monitor_device', on_delete=models.CASCADE)
    options = models.CharField(max_length=50, choices=[], default='')
    state = models.CharField(max_length=50, default='')

    def __str__(self):
        return f"Monitor Device => {self.device.name} (state: {self.state})"

        
