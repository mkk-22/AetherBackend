# TO DO: create the following views
# login
# signup 
# guest login
# 'forgot password' or password reset 
# logout

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import HomeownerSignupForm
from django.contrib.auth import login


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.shortcuts import render

def start_view(request):
    return render(request, 'start.html')



def signup_view(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)  # Default form for user signup
        homeowner_form = HomeownerSignupForm(request.POST)  # Custom form for homeowner details

        if user_form.is_valid() and homeowner_form.is_valid():
            user = user_form.save()  # Save user to the database
            homeowner = homeowner_form.save(commit=False)  # Do not save yet
            homeowner.user = user  # Attach the user to the homeowner model
            homeowner.save()  # Now save the homeowner data

            login(request, user)  # Automatically log the user in
            return redirect('home')  # Redirect to the homepage after signup
        else:
            # If the forms are not valid, render the page with errors
            return render(request, 'signup.html', {'user_form': user_form, 'homeowner_form': homeowner_form})
    else:
        user_form = UserCreationForm()  # Empty form for user signup
        homeowner_form = HomeownerSignupForm()  # Empty form for homeowner details

    return render(request, 'signup.html', {'user_form': user_form, 'homeowner_form': homeowner_form})





from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Default form for login

        if form.is_valid():
            user = form.get_user()  # Get the user based on the credentials
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to the homepage after successful login
        else:
            # If the form is not valid, render the page with errors
            return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()  # Empty form for login

    return render(request, 'login.html', {'form': form})



from django.shortcuts import render, redirect
from .models import Guest

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Guest

def guest_login_view(request):
    if request.method == 'POST':
        guest_code = request.POST.get('guest_code')
        guest_name = request.POST.get('name')

        # Check if the guest code exists
        try:
            guest = Guest.objects.get(guest_code=guest_code)

            # If name is not yet provided, set it now
            if not guest.name:
                guest.name = guest_name
                guest.save()

            # Optionally, check that the guest name matches the one entered
            if guest.name != guest_name:
                messages.error(request, "Name does not match the guest code.")
                return redirect('guest_login')
            
            # If everything is valid, log the guest in
            request.session['guest_id'] = guest.id  # Store guest's ID in session or similar
            return redirect('home')  # Redirect to the home page or wherever appropriate
        except Guest.DoesNotExist:
            messages.error(request, "Invalid guest code.")
            return redirect('guest_login')

    return render(request, 'guest_login.html')



