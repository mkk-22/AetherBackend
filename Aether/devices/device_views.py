from django.shortcuts import render, get_object_or_404, redirect
from .models import House, Room, Device
from users.user_views import generate_unique_code



def roomsanddevices(request):
    house = get_object_or_404(House, house_id=request.user.owner.house_id)
    rooms = house.rooms.all()  
    return render(request, 'roomsanddevices.html', {'house': house, 'rooms': rooms})

from django.utils.crypto import get_random_string

# Function to generate a unique room_id
def generate_unique_room_id():
    return get_random_string(8)  # Generate an 8-character unique string


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

def toggle_device(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)
    device.status = 'off' if device.status == 'on' else 'on'
    device.save()
    return redirect('roomsanddevices')

def see_device_details(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)
    return render(request, 'device_details.html', {'device': device})
