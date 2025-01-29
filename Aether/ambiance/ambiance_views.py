from django.shortcuts import render, get_object_or_404, redirect

from devices.device_views import toggle_device
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
    devices = mode.room.devices.filter(
        general_product_code__in=['AF0005', 'AF0003', 'LF0002', 'AV0001']
    )

    # Create a dictionary for device options
    device_options = {}

    # Populate the device options based on each device
    for device in devices:
        if device.general_product_code == 'AF0005':  
            device_options[device.device_id] = ["red", "gold", "white", "green", "blue", "violet"]
        elif device.general_product_code == 'AF0003':  
            device_options[device.device_id] = ["clean", "sandalwood", "rose", "ocean", "cookie", "eucalyptus", "lemongrass"]
        elif device.general_product_code == 'LF0002':  
            device_options[device.device_id] = ["idle", "pop", "jazz", "classical", "nature sounds", "white noise"]
        elif device.general_product_code == 'AV0001':  
            device_options[device.device_id] = ['16', '24', '27', '32'] 

    if request.method == 'POST':
        # Delete existing ambiance mode devices to ensure only the new ones are saved
        AmbianceModeDevice.objects.filter(mode=mode).delete()

        # Iterate through devices and save new states based on the form submission
        for device in devices:
            device_id = device.device_id
            state = request.POST.get(f'state_{device_id}', '')  # Get the state from the form

            if state:  # Only create an ambiance mode device if a state is selected
                AmbianceModeDevice.objects.create(
                    mode=mode,
                    device=device,
                    state=state,
                )

        return redirect('modes_list')  # Redirect to the modes list after saving changes

    return render(request, 'edit_mode.html', {'mode': mode, 'devices': devices, 'device_options': device_options})


def mode_details(request, mode_id):
    mode = get_object_or_404(AmbianceMode, id=mode_id)
    return render(request, 'mode_details.html', {'mode': mode})

def delete_ambiance_mode(request, mode_id):
    mode = get_object_or_404(AmbianceMode, id=mode_id)
    room_id = mode.room.room_id
    mode.delete()
    return redirect('modes_list')

def toggle_ambiance(request, mode_id):
    mode = get_object_or_404(AmbianceMode, id=mode_id)

    if request.method == 'POST':
        if mode.status == 'off': 
            for device in mode.devices.all():
                if device.device.status == 'off':
                    toggle_device(request, device.device.device_id) 
            mode.status = 'on'
        else:  
            for device in mode.devices.all():
                if device.device.status == 'on':
                    toggle_device(request, device.device.device_id) 
                else:
                    pass

            mode.status = 'off'
            
        mode.save()

    return redirect('modes_list')

