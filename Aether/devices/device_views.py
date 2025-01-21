from django.shortcuts import render, get_object_or_404, redirect
from .models import House, Room, Device


def roomsanddevices(request):
    # Fetch the house by house_id
    house = get_object_or_404(House, house_id=request.user.owner.house_id)
    
    # Get rooms related to the house
    rooms = house.rooms.all()
    
    context = {
        'house': house,
        'rooms': rooms,
    }
    
    return render(request, 'roomsanddevices.html', context)

def add_room(request):
    if request.method == 'POST':
        house = get_object_or_404(House, house_id=request.user.owner.house_id)
        room_name = request.POST['room_name']
        room = Room(house=house, name=room_name)
        room.save()
        return redirect('roomsanddevices', house_id=request.user.owner.house_id)
    return render(request, 'add_room.html')

def remove_room(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    house_id = room.house.house_id
    room.delete()
    return redirect('roomsanddevices', house_id=house_id)

def add_device(request, room_id):
    if request.method == 'POST':
        room = get_object_or_404(Room, room_id=room_id)
        device_id = request.POST['device_id']
        name = request.POST['name']
        general_product_code = request.POST['general_product_code']
        average_energy_consumption_per_hour = request.POST['average_energy_consumption_per_hour']
        status = request.POST['status']

        device = Device(
            device_id=device_id,
            name=name,
            general_product_code=general_product_code,
            average_energy_consumption_per_hour=average_energy_consumption_per_hour,
            status=status,
            room=room
        )
        device.save()
        return redirect('roomsanddevices', house_id=room.house.house_id)
    return render(request, 'add_device.html')

def remove_device(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)
    room = device.room
    house_id = room.house.house_id
    device.delete()
    return redirect('roomsanddevices', house_id=house_id)

def toggle_device(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)
    device.status = 'off' if device.status == 'on' else 'on'
    device.save()
    return redirect('roomsanddevices', house_id=device.room.house.house_id)

def see_device_details(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)
    return render(request, 'device_details.html', {'device': device})
