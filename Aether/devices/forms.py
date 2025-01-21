from django import forms
from .models import Room, Device

class AddRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Room Name'}),
        }


class AddDeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'general_product_code']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Device Name'}),
            'general_product_code': forms.TextInput(attrs={'placeholder': 'General Product Code'}),
            'average_energy_consumption_per_hour': forms.NumberInput(attrs={'placeholder': 'Energy Consumption'}),
        }


class RemoveRoomForm(forms.Form):
    room_id = forms.CharField(widget=forms.HiddenInput())


class RemoveDeviceForm(forms.Form):
    device_id = forms.CharField(widget=forms.HiddenInput())


class ToggleDeviceForm(forms.Form):
    device_id = forms.CharField(widget=forms.HiddenInput())
