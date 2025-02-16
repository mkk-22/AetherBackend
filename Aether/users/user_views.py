from pyexpat.errors import messages
import random
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Owner, User, Guest
from devices.models import House, Room, MonitorFixedDevice, MonitorVariableDevice
from .forms import LoginForm, OwnerSignupForm, GuestLoginForm


def start(request):
    return render(request, 'start.html')

def signup(request):
    if request.method == 'POST':
        form = OwnerSignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            
            house_code = generate_unique_code()
            while Owner.objects.filter(house_id=house_code).exists():
                house_code = generate_unique_code()

            owner = Owner.objects.create(
                user=user,
                plan_type=form.cleaned_data['plan_type'],
                house_id=house_code
            )
            house = House.objects.create(
                owner=owner,
                house_id=house_code, 
            )
            owner.save()
            house.save()
            login(request, user)
            return redirect('tutorial') 
    else:
        form = OwnerSignupForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def tutorial(request):
    return render(request, 'tutorial.html')

@login_required
def guest_tutorial(request):
    return render(request, 'guest_tutorial.html')

def ownerlogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') 
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def guest_login(request):
    if request.method == 'POST':
        form = GuestLoginForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            try:
                guest = Guest.objects.get(code=code, house_id=form.cleaned_data['house_id'])

                # If the guest hasn't set a first name yet (still using "Guest" or None), update it
                if guest.user.first_name is None or guest.user.first_name == "Guest":
                    guest.user.first_name = first_name
                    guest.user.last_name = last_name
                    guest.user.save()

                    # Authenticate the user using the code as the password
                    user = guest.user
                    user = authenticate(request, username=user.username, password=code)

                    if user is not None:
                        login(request, user)
                        return redirect('guest_tutorial')  # Successfully logged in, redirect to guest_home
                    else:
                        form.add_error('code', 'Authentication failed. Please check your code or credentials.')
                else:
                    form.add_error('code', 'This guest code has already been used.')

            except Guest.DoesNotExist:
                form.add_error('code', 'Invalid guest code or house ID.')

    else:
        form = GuestLoginForm()

    return render(request, 'guest_login.html', {'form': form})

@login_required
def home(request):
    # Get latest device states (updated by SimPy)
    updated_device_states = {
        device.device_id: device.state
        for device in MonitorFixedDevice.objects.all()
    }
    updated_device_states.update({
        device.device_id: device.state
        for device in MonitorVariableDevice.objects.all()
    })
    return render(request, 'home.html')
    
@login_required
def my_guests(request):
    guests = Guest.objects.filter(owner=request.user.owner).exclude(user__first_name="Guest")

    if request.method == 'POST':
        guest_id = request.POST.get('guest_id')
        Guest.objects.filter(id=guest_id, owner=request.user.owner).delete()
        return redirect('my_guests')

    return render(request, 'my_guests.html', {'guests': guests})

@login_required
def add_guest(request):
    owner = Owner.objects.get(user=request.user)
    house = get_object_or_404(House, house_id=owner.house_id)
    all_rooms = house.rooms.all()

    current_guest_count = Guest.objects.filter(owner=owner).count()
    guest_limit = 10 if owner.plan_type == 'home' else 75
    if current_guest_count >= guest_limit:
        return render(request, 'my_guests.html', {'error': f'You have reached the guest limit of {guest_limit} guests.'})

    if request.method == 'POST':
        selected_room_ids = request.POST.getlist('rooms')
        departure_date = request.POST.get('departure_date')

        if not selected_room_ids:
            return render(request, 'add_guest.html', {'rooms': all_rooms, 'error': 'Please select at least one room.'})

        code = generate_unique_code()
        while Guest.objects.filter(code=code).exists():
            code = generate_unique_code()
        u_code = generate_unique_code()
        while User.objects.filter(username=u_code).exists():
            u_code = generate_unique_code()

        guest_user = User.objects.create_user(
            username=u_code,
            email="none",
            password=str(code),
            first_name="Guest",
            last_name="User"
        )
        guest = Guest.objects.create(
            owner=owner,
            user=guest_user,
            code=code,
            house_id=owner.house_id,
            departure_date=departure_date
        )

        for room_id in selected_room_ids:
            try:
                room = house.rooms.get(room_id=room_id)
                guest.allowed_rooms.add(room)
            except Room.DoesNotExist:
                print(f"Room with ID {room_id} does not exist.")

        guests = Guest.objects.filter(owner=owner).exclude(user__first_name="Guest")
        return render(request, 'my_guests.html', {'success': f'Guest code {code} generated successfully!', 'code': code, 'house': owner.house_id, 'guests': guests})
    
    return render(request, 'add_guest.html', {'rooms': all_rooms})

def generate_unique_code():
    return random.randint(10000000, 99999999)

@login_required
def guest_home(request):
    try:
        guest = Guest.objects.get(user=request.user)
    except Guest.DoesNotExist:
        return render(request, 'guest_home.html', {'error': 'Guest not found.'})

    allowed_rooms = guest.allowed_rooms.prefetch_related('devices')
    return render(request, 'guest_home.html', {'rooms':allowed_rooms})

@login_required
def settings(request):
    return render(request, 'settings.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('start')

@login_required
def guest_logout_view(request):
    try:
        guest = Guest.objects.get(user=request.user)
        guest_user = request.user
        guest.delete()
        guest_user.delete()
    except Guest.DoesNotExist:
        pass  
    
    logout(request)
    return redirect('start')

def password_reset_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        
        if user:
            return render(request, "password_reset.html", {"reset_sent": True})

        else:
            return render(request, "password_reset.html", {"error": "Email not found."})
    
    return render(request, "password_reset.html")

@login_required
def account(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.email = request.POST.get("email", user.email)
        user.save()
        return redirect("account")  

    return render(request, "account.html")


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()  
        logout(request) 
        return redirect("start")  

    return render(request, "delete_account.html")


def contact_support(request):
    if request.method == "POST":
        return render(request, "contact_support.html", {"success": "We will get back to you within 24 hours, so keep an eye on your email inbox!"})
    
    return render(request, "contact_support.html")