from pathlib import Path
from django.shortcuts import render, get_object_or_404, redirect
from .models import House, Room, Device, FixedOptionDevice, VariableOptionDevice, MonitorDevice
from users.models import Owner
from energy.models import IntervalReading
from django.contrib.auth.decorators import login_required
from users.user_views import generate_unique_code
from django.utils.crypto import get_random_string
import json
from django.http import JsonResponse
from django.utils.timezone import now
from decimal import Decimal

@login_required
def roomsanddevices(request):
    house = get_object_or_404(House, house_id=request.user.owner.house_id)
    rooms = house.rooms.all()

    room_counts = {}
    device_counts = {}

    # Store options per device
    device_options = {}
    updated_device_states = {}

    for room in rooms:
        for device in room.devices.all():
            if device.get_device_type() == 'Fixed':
                fixed_device = device.fixed_device.first()
                if fixed_device:
                    device_options[device.device_id] = fixed_device.options.split(",")
                    updated_device_states[device.device_id] = fixed_device.state

            elif device.get_device_type() == 'Monitor':
                monitor_device = device.monitor_device.first()
                if monitor_device:
                    device_options[device.device_id] = monitor_device.options.split(",")
                    updated_device_states[device.device_id] = monitor_device.state

            elif device.get_device_type() == 'Variable':
                variable_device = device.variable_device.first()
                if variable_device:
                    device_options[device.device_id] = ['State (0-100)']
                    updated_device_states[device.device_id] = variable_device.state

            if room.name in room_counts:
                room_counts[room.name] += 1
            else:
                room_counts[room.name] = 1

            if device.general_product_code in device_counts:
                device_counts[device.general_product_code] += 1
            else:
                device_counts[device.general_product_code] = 1

            room.room_number = room_counts[room.name]
            device.device_number = device_counts[device.general_product_code]
            room.save()
            device.save()

    return render(request, 'roomsanddevices.html', {
        'house': house,
        'rooms': rooms,
        'device_options': device_options,
        'updated_device_states': updated_device_states  # Add this line to pass updated states
    })

def generate_unique_room_id():
    return get_random_string(8)  

@login_required
def add_room(request):
    if request.method == 'POST':
        house = get_object_or_404(House, house_id=request.user.owner.house_id)
        room_name = request.POST.get('room_name', '').strip() 
         
        if not room_name:
            return render(request, 'add_room.html', {'error': 'Room name is required.'})
        
        room_id = generate_unique_room_id()
        while house.rooms.filter(room_id=room_id).exists():
               room_id = generate_unique_code()
        
        last_room = house.rooms.filter(name=room_name).order_by('-room_number').first()
        room_number = last_room.room_number + 1 if last_room else 1  
        
        room = Room.objects.create(name=room_name, house=house, room_id=room_id, room_number=room_number)
        room.save()
        
        return redirect('roomsanddevices')

    return render(request, 'add_room.html')

@login_required
def remove_room(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    room.delete()
    return redirect('roomsanddevices')

@login_required
def add_device(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)

    json_file_path = Path(__file__).resolve().parent / 'devices.json'
    with open(json_file_path, 'r') as f:
        devices_data = json.load(f)

    if request.method == 'POST':
        general_product_code = request.POST['general_product_code']
        
        device_data = next((d for d in devices_data if d['general_product_code'] == general_product_code), None)
        if not device_data:
            return JsonResponse({"error": "Invalid product code"}, status=400)

        device_id = generate_unique_code()
        while room.devices.filter(device_id=device_id).exists():  
               device_id = generate_unique_code()

        last_device = room.devices.filter(general_product_code=general_product_code).order_by('-device_number').first()
        device_number = last_device.device_number + 1 if last_device else 1  

        device = Device(
            device_id=device_id,
            name=device_data['name'],
            general_product_code=general_product_code,
            manufacturer=device_data.get('manufacturer', ''),
            average_energy_consumption_per_hour=device_data.get('average_energy_consumption_per_hour', 1),
            status='on',
            room=room,
            device_number=device_number  
        )
        device.save()
        
        device_type = device.get_device_type()
        
        if device_type == 'Fixed':
            options = device_data.get('options', [])  
            FixedOptionDevice.objects.create(
                device=device,
                options=options if options else '',
                state= 'none'
            )
        elif device_type == 'Variable':
            VariableOptionDevice.objects.create(
                device=device,
                state=25
            )
        elif device_type == 'Monitor':
            options = device_data.get('options', ['default'])  
            MonitorDevice.objects.create(
                device=device,
                options=options,
                state= options[0]  
            )
            
        return redirect('roomsanddevices')

    return render(request, 'add_device.html')

@login_required
def remove_device(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)
    device.delete()
    return redirect('roomsanddevices')

@login_required
def toggle_device(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)
    
    if device.status == 'off':  
        IntervalReading.objects.create(
            device_id=device.device_id,
            homeowner=device.room.house.owner,  
            start=now()
        )
        device.status = 'on'  
    else: 
        interval = IntervalReading.objects.filter(
            device_id=device.device_id,
            end__isnull=True  
        ).first()

        if interval:  
            interval.end = now()
            interval.usage = calculate_usage(interval)
            interval.save()
        device.status = 'off' 

    device.save()

    if hasattr(request.user, 'guest'):  
        return redirect('guest_home')  
    else:
        return redirect('roomsanddevices') 

def calculate_usage(interval):
    duration_in_hours = (interval.end - interval.start).total_seconds() / 3600
    device = Device.objects.get(device_id=interval.device_id)
    average_consumption = Decimal(device.average_energy_consumption_per_hour)
    usage = Decimal(duration_in_hours) * average_consumption
    return usage

@login_required
def update_device_state(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)

    if device.status == 'on':
        if device.get_device_type() == 'Fixed':
            selected_option = request.POST.get('fixed_option')
            fixed_device = get_object_or_404(FixedOptionDevice, device=device)
            if fixed_device:
                fixed_device.state = selected_option
                fixed_device.save()

        elif device.get_device_type() == 'Monitor':
            selected_option = request.POST.get('monitor_option')

            monitor_device = get_object_or_404(MonitorDevice, device=device)
            if monitor_device:
                monitor_device.state = selected_option
                monitor_device.save()

        elif device.get_device_type() == 'Variable':
            state_value = request.POST.get('variable_state')
            try:
                state_value = int(state_value)
                variable_device = get_object_or_404(VariableOptionDevice, device=device)
                if variable_device:
                    variable_device.state = state_value
                    variable_device.save()
            except ValueError:
                pass  

    return redirect('roomsanddevices')

@login_required
def device_info(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)
    device_type = device.get_device_type()
    state = ''
    
    if device_type == 'Fixed':
        state = get_object_or_404(FixedOptionDevice, device=device).state
    elif device_type == 'Variable':
        state = get_object_or_404(VariableOptionDevice, device=device).state
    elif device_type == 'Monitor':
        state = get_object_or_404(MonitorDevice, device=device).state
    else:
        pass

    return render(request, 'device_info.html', {'device': device, 'state': state})
