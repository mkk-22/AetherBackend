from pyexpat.errors import messages
import random
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Owner, User, Guest
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

            return redirect('ownerlogin') 
    else:
        form = OwnerSignupForm()
    return render(request, 'signup.html', {'form': form})

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
                # Retrieve the guest by both code and house_id
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
                        return redirect('guest_home')  # Successfully logged in, redirect to guest_home
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
    return render(request, 'home.html')
    
@login_required
def my_guests(request):
    return render(request, 'my_guests.html')

@login_required
def generate_guest_code(request):
    owner = Owner.objects.get(user=request.user)

    print("FAIL")
    current_guest_count = Guest.objects.filter(owner=owner).count()
    print(str(current_guest_count))
    if owner.plan_type == 'home':
        guest_limit = 10
    else:
        guest_limit = 75
    print(str(guest_limit))
    if current_guest_count >= guest_limit:
        print("No")
        return render(request, 'my_guests.html', {'error': f'You have reached the guest limit of {guest_limit} guests.'})

    code = generate_unique_code()
    while Guest.objects.filter(code=code).exists():
        code = generate_unique_code()

    guest_user = User.objects.create_user(
        username=str(code), 
        email="none", 
        password=str(code),  
        first_name="Guest",  
        last_name="User" 
    )

    Guest.objects.create(
        owner=owner,
        user=guest_user,
        code=code,
        house_id=owner.house_id 
    )

    print(str(owner.house_id))
    return render(request, 'my_guests.html', {'success': f'Guest code {code} generated successfully!', 'code': code})

def generate_unique_code():
    return random.randint(10000000, 99999999)

@login_required
def guest_home(request):
    return render(request, 'guest_home.html')

@login_required
def logout_view(request):
