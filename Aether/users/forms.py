from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.models import HomeOwner
from energy.models import EnergyGoal

# 1. User Signup Form (Django's built-in form)
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Ensures email is included in the form

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Fields from the User model

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

# 2. Homeowner Signup Form (Custom form for Homeowner details)
class HomeownerSignupForm(forms.ModelForm):
    plan_type = forms.ChoiceField(choices=HomeOwner.PLAN_CHOICES, required=True)
    energy_goal = forms.ModelChoiceField(queryset=EnergyGoal.objects.all(), required=True)

    class Meta:
        model = HomeOwner
        fields = ['plan_type', 'energy_goal']  # Fields specific to Homeowner model
