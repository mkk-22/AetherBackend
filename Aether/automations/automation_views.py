from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Automation
from devices.models import Device, House, Room
from users.models import Owner
from django.contrib.auth.decorators import login_required
import json

@login_required
def automations_list(request):
    automations = Automation.objects.all()
    return render(request, 'automations_list.html', {'automations': automations})

@login_required
@login_required
def add_automation(request):
    house = get_object_or_404(House, house_id=request.user.owner.house_id)
    rooms = house.rooms.all() 
    devices_by_room = {room.room_id: list(Device.objects.filter(room=room).values('device_id', 'name')) for room in rooms}
    
    devices_by_room_json = json.dumps(devices_by_room)

    if request.method == 'POST':
        name = request.POST['name']
        trigger_time = request.POST['trigger_time']
        devices_on_ids = request.POST.getlist('devices_on')  # Getting the device IDs for "on"
        devices_off_ids = request.POST.getlist('devices_off')  # Getting the device IDs for "off"

        devices_on = Device.objects.filter(device_id__in=devices_on_ids)
        devices_off = Device.objects.filter(device_id__in=devices_off_ids)

        if devices_on or devices_off:
            automation = Automation.objects.create(
                name=name,
                trigger_time=trigger_time
            )

            automation.devices_on.set(devices_on)
            automation.devices_off.set(devices_off)
            automation.save()

            return redirect('automations_list')

    return render(request, 'add_automation.html', {'rooms': rooms, 'devices_by_room_json': devices_by_room_json})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Automation, Device

@login_required
def edit_automation(request, automation_id):
    # Fetch the automation object or return 404 if not found
    automation = get_object_or_404(Automation, id=automation_id)
    
    # Get all devices for room selection
    devices = Device.objects.all()

    if request.method == 'POST':
        # Get form data
        name = request.POST['name']
        trigger_time = request.POST['trigger_time']
        devices_on_ids = request.POST.getlist('devices_on')  # Devices that should be turned on
        devices_off_ids = request.POST.getlist('devices_off')  # Devices that should be turned off

        # Fetch devices from the database using device_ids
        devices_on = Device.objects.filter(id__in=devices_on_ids)
        devices_off = Device.objects.filter(id__in=devices_off_ids)

        # Check if devices are selected before updating the automation
        if devices_on or devices_off:
            automation.name = name
            automation.trigger_time = trigger_time
            # Set the devices to the automation (many-to-many fields)
            automation.devices_on.set(devices_on)
            automation.devices_off.set(devices_off)
            automation.save()

            # Redirect to automations list after saving
            return redirect('automations_list')
        else:
            # Handle the case where no devices are selected
            error_message = "Please select at least one device."
            return render(request, 'edit_automation.html', {
                'automation': automation,
                'devices': devices,
                'error_message': error_message
            })

    return render(request, 'edit_automation.html', {'automation': automation, 'devices': devices})

@login_required
def automation_details(request, automation_id):
    automation = get_object_or_404(Automation, id=automation_id)
    return render(request, 'automation_details.html', {'automation': automation})

@login_required
def delete_automation(request, automation_id):
    automation = get_object_or_404(Automation, id=automation_id)
    automation.delete()
    return redirect('automations_list')


