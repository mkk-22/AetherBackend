"""
URL configuration for Aether project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import user_views
from devices import device_views
from energy import energy_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.start, name='start'),
    path('signup/', user_views.signup, name='signup'),
    path('login/', user_views.ownerlogin, name='ownerlogin'),
    path('guest_login/', user_views.guest_login, name='guest_login'),
    path('home/', user_views.home, name='home'),
    path('my_guests/', user_views.my_guests, name='my_guests'),
    path('generate_guest_code/', user_views.generate_guest_code, name='generate_guest_code'),
    path('guest_home/',user_views.guest_home, name='guest_home'),
    path('logout/', user_views.logout_view, name='logout'),
    
    path('roomsanddevices/<str:house_id>/', device_views.roomsanddevices, name='roomsanddevices'),
    path('roomsanddevices/', device_views.roomsanddevices, name='roomsanddevices'),
    path('add_room/', device_views.add_room, name='add_room'),
    path('remove_room/<str:room_id>/', device_views.remove_room, name='remove_room'),
    path('remove_room/', device_views.remove_room, name='remove_room'),
    path('add_device/<str:room_id>/', device_views.add_device, name='add_device'),
    path('add_device/', device_views.add_device, name='add_device'),
    path('remove_device/<int:device_id>/', device_views.remove_device, name='remove_device'),
    path('toggle_device/<int:device_id>/', device_views.toggle_device, name='toggle_device'),
    path('toggle_device/', device_views.toggle_device, name='toggle_device'),
    path('see_device_details/', device_views.see_device_details, name='see_device_details'),
    
    path('energy_home/', energy_views.energy_home, name='energy_home'),
    path('set_goal/', energy_views.set_goal, name='set_goal'),
    path('remove_goal/', energy_views.remove_goal, name='remove_goal'),
    path('usage_stats/', energy_views.usage_stats, name='usage_stats'),
    path('join-event/<int:event_id>/', energy_views.join_event, name='join_event')
]
