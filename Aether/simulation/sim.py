import random
import time
import simpy
import django
import os
import threading

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Aether.settings")
django.setup()

from devices.models import MonitorFixedDevice, MonitorVariableDevice
from users.models import User


class Simulation:
    def __init__(self):
        self.env = simpy.Environment()
        self.env.process(self.device_simulation())  # Start the simulation process

    def device_simulation(self):
        while True:
            self.update_monitor_fixed_devices()
            self.update_monitor_variable_devices()
            print("NOw")
            time.sleep(5)

    def update_monitor_fixed_devices(self):
        for device in MonitorFixedDevice.objects.all():
            device.state = random.choice(device.options.split(", "))  # Change the state randomly
            device.save()

    def update_monitor_variable_devices(self):
        for device in MonitorVariableDevice.objects.all():
            device.state = random.randint(20, 100)  # Random integer value
            device.save()

    def run(self):
        """Start the simulation process."""
        self.env.run()  # Run the simulation environment, which will wait for the timeout to occur


# Create a thread to run the simulation
def start_simulation():
    print("Starting SimPy simulation...")
    simulation = Simulation()  # Create the simulation
    simulation.run()  # Run it once, properly handling timeouts


def run_simulation():
    sim = Simulation()
    sim.run()


# Start the simulation thread (this should start the simulation in the background)
simulation_thread = threading.Thread(target=start_simulation, daemon=True)
simulation_thread.start()
