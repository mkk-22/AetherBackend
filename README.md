# Aether

Description of the structure:
1. Aether: this is the main project file
2. Apps (so far): 
    - users: login, signup, guest login, logout
    - devices: add/remove rooms/ add/remove devices in rooms, toggle devices, create interval reading records
    - energy: set/remove a daily energy consumption goal, view stats, project bill, usage, view and join/leave community events
    - ambience: view ambience mode of a room, add/edit/remove modes
    - automation: view automations, add/edit/remove automations
    - devicesharing: device sharing platform, search for available device, add listing, request device, approve/decline pending requests
    - virtualenv: virtual environment detection and toggle suggetsion functionality
    - notifs: detect urgent changes, alert user
    - simulation: change state of devices randomly to simulate real-life 


How to host locally:
1. activate venv using 'source venv/bin/activate'
2. create superuser using 'python manage.py createsuperuser', 
and set your preferred credentials (I use username: admin, password: 1234567890)
2. use 'python manage.py runserver' to start session
3. the site can be opened on link 'http://127.0.0.1:8000/' 
and the admin panel can be accessed on 'http://127.0.0.1:8000/admin/'
