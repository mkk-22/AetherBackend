from pathlib import Path
from django.shortcuts import render, get_object_or_404, redirect
from .models import House, Room, Device
from energy.models import IntervalReading
from django.contrib.auth.decorators import login_required
from users.user_views import generate_unique_code
from django.utils.crypto import get_random_string
from django.utils import timezone


from django.shortcuts import render, get_object_or_404
from .models import House

from django.shortcuts import render, get_object_or_404
from .models import House

from django.shortcuts import render, get_object_or_404
from .models import House

def roomsanddevices(request):
    house = get_object_or_404(House, house_id=request.user.owner.house_id)
    rooms = house.rooms.all()

    # Create a dictionary to store the count of devices per model (across the entire house)
    device_counts = {}

    # Iterate through the rooms and devices
    for room in rooms:
        for device in room.devices.all():
            # Increment the count for the device's model (general_product_code)
            if device.general_product_code in device_counts:
                device_counts[device.general_product_code] += 1
            else:
                device_counts[device.general_product_code] = 1
            
            # Assign a unique device number for this model within the house
            device.device_number = device_counts[device.general_product_code]
            device.save()

            # Debugging: Print out the device and its device number
            print(f"Device: {device.name}, Model Code: {device.general_product_code}, Device Number: {device.device_number}")

    # Pass rooms and the updated devices to the template
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

import json
from django.shortcuts import get_object_or_404, redirect, render
from .models import Device
from django.http import JsonResponse


def add_device(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)

    # Path to the JSON file
    json_file_path = Path(__file__).resolve().parent / 'devices.json'

    # Load JSON data
    with open(json_file_path, 'r') as f:
        devices_data = json.load(f)

    if request.method == 'POST':
        general_product_code = request.POST['general_product_code']
        
        # Match product code in JSON file
        device_data = next((d for d in devices_data if d['general_product_code'] == general_product_code), None)
        if not device_data:
            return JsonResponse({"error": "Invalid product code"}, status=400)

        # Generate unique device_id
        device_id = generate_unique_code()

        # Find the last device with the same general_product_code in the room
        last_device = room.devices.filter(general_product_code=general_product_code).order_by('-device_number').first()
        device_number = last_device.device_number + 1 if last_device else 1  # Start from 1 for the first device

        # Create Device
        device = Device(
            device_id=device_id,
            name=device_data['name'],
            general_product_code=general_product_code,
            manufacturer=device_data.get('manufacturer', ''),
            average_energy_consumption_per_hour=device_data.get('average_consumption', 10),
            status='off',
            room=room,
            device_number=device_number  # Set the device number
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

def device_info(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)
    return render(request, 'device_info.html', {'device': device})
