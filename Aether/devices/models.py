from django.db import models


# TO DO: 
# create the following models:
#   - Device: ID, name, type (room?), status (on/off/idle/error), avg energy per hour, hours used since Jan 1, owner ID
#   - AmbienceMode: ID, name, device list, status (on/off/error), owner ID
#   - Automation: ID, name, trigger condition, steps (list of {device ID, action, delay} tuples), current step,
#         status (on/off/pause/error), owner ID
#   - AvailableDevice: Device ID, owner ID
#   - DeviceRequest: ID, request-er ID, owner ID, start date, end date, status (pending/approved/overdue)
#   - VirtualEnv: ID, Ambience ID, goal condition 
#
# AND register any custom models in the main projects 'settings.py'
# AND register the models in the main projects 'admin.py'


