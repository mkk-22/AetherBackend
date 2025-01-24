from django.shortcuts import render, get_object_or_404, redirect
from .models import Automation
from devices.models import Device

def automations_list(request):
    automations = Automation.objects.all()
    return render(request, 'automations_list.html', {'automations': automations})

def add_automation(request):
    devices = Device.objects.all()

    if request.method == 'POST':
        print("Form received")
        
        # Collecting form data
        name = request.POST['name']
        trigger_type = request.POST['trigger_type']
        trigger_value = request.POST['trigger_value']
        selected_devices = request.POST.getlist('devices')

        # Debugging selected devices
        print(f"Selected devices: {selected_devices}")
        
        # Ensure devices exist and are valid
        selected_devices = Device.objects.filter(device_id__in=selected_devices)
        
        # Debugging found devices
        print(f"Devices found: {selected_devices}")
        
        # Only proceed if at least one device was selected
        if selected_devices:
            print("About to create automation...")

            # Create and save the automation
            automation = Automation.objects.create(
                name=name,
                trigger_type=trigger_type,
                trigger_value=trigger_value
            )
            print("Created 1/2")

            automation.devices.set(selected_devices)
            print("Created 2/2")

            automation.save()
            print("Automation created!")

            return redirect('automations_list')

        else:
            print("No valid devices found!")

    print("Failed")
    return render(request, 'add_automation.html', {'devices': devices})




def edit_automation(request, automation_id):
    automation = get_object_or_404(Automation, id=automation_id)
    devices = Device.objects.all()

    if request.method == 'POST':
        # Get the updated data from the form
        name = request.POST['name']
        trigger_type = request.POST['trigger_type']
        trigger_value = request.POST['trigger_value']
        selected_devices = request.POST.getlist('devices')

        print("Selected devices (POST):", selected_devices)

        # Ensure devices exist and are valid
        selected_devices = Device.objects.filter(device_id__in=selected_devices)
        print("Devices found:", selected_devices)

        if selected_devices:
            automation.name = name
            automation.trigger_type = trigger_type
            automation.trigger_value = trigger_value
            automation.devices.set(selected_devices)  # Update the many-to-many relationship
            automation.save()
            print("Automation updated!")
            return redirect('automations_list')

        print("No valid devices found!")
    
    return render(request, 'edit_automation.html', {'automation': automation, 'devices': devices})



def delete_automation(request, automation_id):
    automation = get_object_or_404(Automation, id=automation_id)
    automation.delete()
    return redirect('automations_list')
