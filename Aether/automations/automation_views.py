from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Automation
from devices.models import Device, Room
from django.contrib.auth.decorators import login_required
import json

@login_required
def automations_list(request):
    automations = Automation.objects.all()
    return render(request, 'automations_list.html', {'automations': automations})

@login_required
def add_automation(request):
    # Get all rooms and devices
    rooms = Room.objects.all()
    devices_by_room = {}

    # Create a dictionary of devices for each room, but convert them to serializable data
    for room in rooms:
        devices_by_room[room.room_id] = list(Device.objects.filter(room=room).values('device_id', 'name'))

    print(devices_by_room)
    
    # Pass the devices_by_room to the template
    devices_by_room_json = json.dumps(devices_by_room)

    if request.method == 'POST':
        name = request.POST['name']
        trigger_time = request.POST['trigger_time']
        devices_on_ids = request.POST.getlist('devices_on')
        devices_off_ids = request.POST.getlist('devices_off')

        devices_on = Device.objects.filter(id__in=devices_on_ids)
        devices_off = Device.objects.filter(id__in=devices_off_ids)

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

@login_required
def edit_automation(request, automation_id):
    automation = get_object_or_404(Automation, id=automation_id)
    devices = Device.objects.all()

    if request.method == 'POST':
        name = request.POST['name']
        trigger_time = request.POST['trigger_time']
        devices_on_ids = request.POST.getlist('devices_on')
        devices_off_ids = request.POST.getlist('devices_off')

        devices_on = Device.objects.filter(device_id__in=devices_on_ids)
        devices_off = Device.objects.filter(device_id__in=devices_off_ids)

        if devices_on or devices_off:
            automation.name = name
            automation.trigger_time = trigger_time
            automation.devices_on.set(devices_on)
            automation.devices_off.set(devices_off)
            automation.save()

            return redirect('automations_list')

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


