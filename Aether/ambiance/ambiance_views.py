from django.shortcuts import render, get_object_or_404, redirect
from .models import AmbianceMode, AmbianceModeDevice
from devices.models import House, Room, Device



def modes_list(request):
    house = get_object_or_404(House, house_id=request.user.owner.house_id)
    rooms = house.rooms.all()    
    return render(request, 'modes_list.html', {'house': house, 'rooms': rooms})

def add_ambiance_mode(request):
    house = get_object_or_404(House, house_id=request.user.owner.house_id)
    rooms = house.rooms.all()  

    if request.method == 'POST':
        name = request.POST.get('name')
        room_id = request.POST.get('room')  
        room = get_object_or_404(Room, id=room_id) 

        AmbianceMode.objects.create(room=room, name=name)
        return redirect('modes_list')

    return render(request, 'add_mode.html', {'house': house, 'rooms': rooms})

def edit_ambiance_mode(request, mode_id):
    mode = get_object_or_404(AmbianceMode, id=mode_id)
    devices = mode.room.devices.all()

    if request.method == 'POST':
        # Clear existing device settings for this mode
        mode.devices.all().delete()

        # Add new devices with settings
        for device_id in request.POST.getlist('device_id'):
            device = get_object_or_404(Device, device_id=device_id)
            light_color = request.POST.get(f'light_color_{device_id}')
            volume = request.POST.get(f'volume_{device_id}')
            temperature = request.POST.get(f'temperature_{device_id}')
            status = request.POST.get(f'status_{device_id}', 'off')

            AmbianceModeDevice.objects.create(
                mode=mode,
                device=device,
                light_color=light_color or None,
                volume=volume or None,
                temperature=temperature or None,
                status=status,
            )
        return redirect('modes_list')

    return render(request, 'edit_mode.html', {'mode': mode, 'devices': devices})

def mode_details(request, mode_id):
    mode = get_object_or_404(AmbianceMode, id=mode_id)
    return render(request, 'mode_details.html', {'mode': mode})

def delete_ambiance_mode(request, mode_id):
    mode = get_object_or_404(AmbianceMode, id=mode_id)
    room_id = mode.room.room_id
    mode.delete()
    return redirect('modes_list')
