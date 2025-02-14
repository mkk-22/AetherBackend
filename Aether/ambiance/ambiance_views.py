from django.shortcuts import render, get_object_or_404, redirect

from devices.device_views import toggle_device
from .models import AmbianceMode, AmbianceModeDevice
from devices.models import House, Room, Device, FixedOptionDevice, VariableOptionDevice



def modes_list(request):
    house = get_object_or_404(House, house_id=request.user.owner.house_id)
    rooms = house.rooms.all()  
    rooms = Room.objects.filter(house=house, devices__general_product_code__in=['AF0005', 'AF0003', 'LF0002', 'AV0001']).distinct()

    return render(request, 'modes_list.html', {'house': house, 'rooms': rooms})

def add_ambiance_mode(request):
    house = get_object_or_404(House, house_id=request.user.owner.house_id)
    rooms = Room.objects.filter(house=house, devices__general_product_code__in=['AF0005', 'AF0003', 'LF0002', 'AV0001']).distinct() 

    if request.method == 'POST':
        name = request.POST.get('name')
        room_id = request.POST.get('room')  
        room = get_object_or_404(Room, room_id=room_id) 

        mode = AmbianceMode.objects.create(room=room, name=name)
        return redirect('edit_ambiance_mode', mode_id=mode.id) 

    return render(request, 'add_mode.html', {'house': house, 'rooms': rooms})


def edit_ambiance_mode(request, mode_id):
    mode = get_object_or_404(AmbianceMode, id=mode_id)
    devices = mode.room.devices.filter(
        general_product_code__in=['AF0005', 'AF0003', 'LF0002', 'AV0001']
    )

    # Fetch existing device states for this ambiance mode
    existing_states = {
        amd.device.device_id: amd.state for amd in AmbianceModeDevice.objects.filter(mode=mode)
    }
    print(existing_states)

    # Define options for each device type
    device_options = {
        'AF0005': ["red", "gold", "white", "green", "blue", "violet"],
        'AF0003': ["clean", "sandalwood", "rose", "ocean", "cookie", "eucalyptus", "lemongrass"],
        'LF0002': ["idle", "pop", "jazz", "classical", "nature sounds", "white noise"],
        'AV0001': ['16', '24', '27', '32']
    }

    if request.method == 'POST':
        # Clear existing device states for this mode
        AmbianceModeDevice.objects.filter(mode=mode).delete()

        # Save new states
        for device in devices:
            device_id = device.device_id
            state = request.POST.get(f'state_{device_id}', '')  # Get from form

            if state:  # Only save if a state is selected
                AmbianceModeDevice.objects.create(
                    mode=mode,
                    device=device,
                    state=state,
                    prev_state=existing_states.get(device_id, ''),  # Save previous state
                    prev_status=device.status
                )

        return redirect('mode_details', mode_id=mode.id)

    return render(request, 'edit_mode.html', {
        'mode': mode,
        'devices': devices,
        'device_options': {device.device_id: device_options.get(device.general_product_code, []) for device in devices},
        'existing_states': existing_states  # Pass previous states to template
    })


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
            for ambiance_device in mode.devices.all():
                base_device = ambiance_device.device

                ambiance_device.prev_status = base_device.status

                # Try to get the specific device type (FixedOptionDevice or VariableOptionDevice)
                fixed_device = FixedOptionDevice.objects.filter(device=base_device).first()
                variable_device = VariableOptionDevice.objects.filter(device=base_device).first()

                if fixed_device:
                    print("its fixed")
                    ambiance_device.prev_state = fixed_device.state.replace(' ', '')  # Store previous state (string)
                    fixed_device.state = ambiance_device.state.replace(' ', '')  # Apply ambiance mode state
                    fixed_device.save()
                    print("new state: "+fixed_device.state)

                elif variable_device:
                    print("its variable")
                    ambiance_device.prev_state = str(variable_device.state) if variable_device.state is not None else "0"
                    variable_device.state = ambiance_device.state  # Apply ambiance mode state
                    variable_device.save()
                    print("new state: "+str(variable_device.state))

                # Turn device ON
                base_device.status = 'on'
                base_device.save()
                ambiance_device.save()

            mode.status = 'on'

        else:  # Turning ambiance mode OFF
            for ambiance_device in mode.devices.all():
                base_device = ambiance_device.device

                # Restore previous status
                base_device.status = ambiance_device.prev_status

                # Restore previous state if applicable
                fixed_device = FixedOptionDevice.objects.filter(device=base_device).first()
                variable_device = VariableOptionDevice.objects.filter(device=base_device).first()

                if fixed_device:
                    fixed_device.state = ambiance_device.prev_state  # Restore previous state (string)
                    fixed_device.save()

                elif variable_device:
                    if ambiance_device.prev_state and ambiance_device.prev_state.isdigit():
                        variable_device.state = int(ambiance_device.prev_state)  # Convert stored string back to int
                    else:
                        variable_device.state = 0  # Default fallback state
                    variable_device.save()

                base_device.save()
                ambiance_device.save()

            mode.status = 'off'

        mode.save()

    return redirect('modes_list')