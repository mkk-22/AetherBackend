import random
import simpy
import django
import os
import threading

# Ensure Django is fully loaded
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Aether.settings")
django.setup()

from devices.models import MonitorFixedDevice, MonitorVariableDevice
from notifs.models import Notification
from users.models import User
from virtualenv.models import VirtualEnv


class Simulation:
    def __init__(self):
        self.env = simpy.Environment()
        self.env.process(self.device_simulation())

    def device_simulation(self):
        while True:
            self.update_monitor_fixed_devices()
            self.update_monitor_variable_devices()
            #self.check_environment_conditions()
            yield self.env.timeout(60)  # Wait 15 seconds before running again

    def update_monitor_fixed_devices(self):
        for device in MonitorFixedDevice.objects.all():
            device.state = random.choice(device.options.split(", "))
            device.save()

    def update_monitor_variable_devices(self):
        for device in MonitorVariableDevice.objects.all():
            device.state = random.randint(20, 100)
            device.save()

    def check_environment_conditions(self):
        for virtual_env in VirtualEnv.objects.all():
            if self.check_conditions(virtual_env):
                self.create_notification(virtual_env)

    def check_conditions(self, virtual_env):
        current_temp = self.get_current_temperature()
        current_humidity = self.get_current_humidity()
        current_light = self.get_current_light()

        return (current_temp >= virtual_env.temperature_condition and
                current_humidity >= virtual_env.humidity_condition and
                current_light >= virtual_env.light_condition)

    def create_notification(self, virtual_env):
        user = self.get_user_for_notification()
        if user:
            message = f"The {virtual_env.name} conditions have been met."
            Notification.objects.create(user=user, message=message)

    def get_current_temperature(self):
        return 25.0

    def get_current_humidity(self):
        return 60.0

    def get_current_light(self):
        return 80.0

    def get_user_for_notification(self):
        return User.objects.first()

    def run(self):
        """Runs the simulation continuously."""
        while True:
            self.env.run()


# Create a thread to run the simulation
def start_simulation():
    print("Starting SimPy simulation...")
    simulation = Simulation()
    simulation.run()
    
def run_simulation():
    sim = Simulation()
    sim.run()

simulation_thread = threading.Thread(target=start_simulation, daemon=True)
simulation_thread.start()