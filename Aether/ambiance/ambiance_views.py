from django.shortcuts import render, get_object_or_404, redirect
from .models import AmbianceMode, AmbianceModeDevice
from devices.models import Room, Device


def ambiance_modes(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    modes = room.modes.all()
    return render(request, 'modes_list.html', {'room': room, 'modes': modes})


def add_ambiance_mode(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        AmbianceMode.objects.create(room=room, name=name)
        return redirect('ambiance_modes', room_id=room_id)

    return render(request, 'add_mode.html', {'room': room})


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
        return redirect('ambiance_modes', room_id=mode.room.room_id)

    return render(request, 'edit_mode.html', {'mode': mode, 'devices': devices})


def delete_ambiance_mode(request, mode_id):
    mode = get_object_or_404(AmbianceMode, id=mode_id)
    room_id = mode.room.room_id
    mode.delete()
    return redirect('ambiance_modes', room_id=room_id)
