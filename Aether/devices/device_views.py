from django.shortcuts import render, get_object_or_404, redirect
from .models import House, Room, Device
from energy.models import IntervalReading
from django.contrib.auth.decorators import login_required
from users.user_views import generate_unique_code
from django.utils.crypto import get_random_string
from django.utils import timezone


def roomsanddevices(request):
    house = get_object_or_404(House, house_id=request.user.owner.house_id)
    rooms = house.rooms.all()  
    return render(request, 'roomsanddevices.html', {'house': house, 'rooms': rooms})

def generate_unique_room_id():
    return get_random_string(8)  

def add_room(request):
    if request.method == 'POST':
        # Debug: Print POST data
        print("POST data:", request.POST)

        # Fetch the house using the house_id from the owner
        house = get_object_or_404(House, house_id=request.user.owner.house_id)

        # Get the room name from the form and validate it
        room_name = request.POST.get('room_name', '').strip()  # Default to empty if not provided
        print("Room name:", room_name)  # Debug: Print room name

        if not room_name:
            # If no room name is provided, return an error message
            return render(request, 'add_room.html', {'error': 'Room name is required.'})

        room_id = generate_unique_room_id()

        # Create the new room
        room = Room.objects.create(name=room_name, house=house, room_id=room_id)

        # Debug: Print room object to confirm creation
        print("Room object created:", room)

        # Redirect back to the rooms and devices page
        return redirect('roomsanddevices')

    return render(request, 'add_room.html')

def remove_room(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    house_id = room.house.house_id
    room.delete()
    return redirect('roomsanddevices')

def add_device(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    if request.method == 'POST':
        device_id = generate_unique_code()
        name = "device"
        general_product_code = request.POST['general_product_code']
        average_energy_consumption_per_hour = 10
        status = "off"

        device = Device(
            device_id=device_id,
            name=name,
            general_product_code=general_product_code,
            average_energy_consumption_per_hour=average_energy_consumption_per_hour,
            status=status,
            room=room
        )
        device.save()
        return redirect('roomsanddevices')
    return render(request, 'add_device.html')

def remove_device(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)
    room = device.room
    house_id = room.house.house_id
    device.delete()
    return redirect('roomsanddevices')

from django.utils.timezone import now

@login_required
def toggle_device(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)
    
    if device.status == 'off':  # Toggling the device ON
        IntervalReading.objects.create(
            device_id=device.device_id,
            homeowner=request.user.owner,  
            start=now()
        )
        device.status = 'on'  # Update the status to 'on'
    else:  # Toggling the device OFF
        interval = IntervalReading.objects.filter(
            device_id=device.device_id,
            end__isnull=True  
        ).first()

        if interval:  # Ensure there's an open interval
            interval.end = now()
            interval.usage = calculate_usage(interval)
            interval.save()
        device.status = 'off'  # Update the status to 'off'

    device.save()
    return redirect('roomsanddevices')


from decimal import Decimal
from django.utils.timezone import timedelta

def calculate_usage(interval):
    # Convert the difference between start and end to hours
    duration_in_hours = (interval.end - interval.start).total_seconds() / 3600

    device = Device.objects.get(device_id=interval.device_id)
    
    # Ensure device.average_energy_per_hour is Decimal
    average_consumption = Decimal(device.average_energy_consumption_per_hour)

    # Calculate usage as a Decimal
    usage = Decimal(duration_in_hours) * average_consumption
    return usage


def see_device_details(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)
    return render(request, 'device_details.html', {'device': device})
