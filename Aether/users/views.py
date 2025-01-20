from pyexpat.errors import messages
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
            owner = Owner.objects.create(
                user=user,
                plan_type=form.cleaned_data['plan_type']
            )
            try:
                trial_owner = owner
            except trial_owner.DoesNotExist:
                return redirect('signup')  
            
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
            name = form.cleaned_data['name']
            try:
                guest = Guest.objects.get(code=code, name__isnull=True) 
                guest.name = name
                guest.save()
                return redirect('guest_home')  
            except Guest.DoesNotExist:
                form.add_error('code', 'Invalid or already used guest code')
    else:
        form = GuestLoginForm()

    return render(request, 'guest_login.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')
    
@login_required
def generate_guest_code(request):
    owner = Owner.objects.get(user=request.user)
    if owner.plan_type == 'home':
        guest_limit = 10
    else:
        guest_limit = 75

    current_guest_count = Guest.objects.filter(owner=owner, name__isnull=True).count()

    if current_guest_count >= guest_limit:
        return render(request, 'home.html', {'error': f'You have reached the guest limit of {guest_limit} guests.'})

    # Generate guest code
    code = None
    if request.method == 'GET':
        code = generate_unique_code()

        # Ensure the code is unique
        while Guest.objects.filter(code=code).exists():
            code = generate_unique_code()

        # Save the guest code in the database
        Guest.objects.create(owner=owner, code=code)

    return render(request, 'home.html', {'success': f'Guest code {code} generated successfully!', 'code': code})

def generate_unique_code():
    import random
    return str(random.randint(1000, 9999))

@login_required
def guest_home(request):
    return render(request, 'guest_home.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('start')