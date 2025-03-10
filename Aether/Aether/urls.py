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
from ambiance import ambiance_views
from automation import automation_views
from devicesharing import ds_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.start, name='start'),
    path('signup/', user_views.signup, name='signup'),
    path('tutorial/', user_views.tutorial, name='tutorial'),
    path('guest_tutorial/', user_views.guest_tutorial, name='guest_tutorial'),
    path('login/', user_views.ownerlogin, name='ownerlogin'),
    path('guest_login/', user_views.guest_login, name='guest_login'),
    path('home/', user_views.home, name='home'),
    path('my_guests/', user_views.my_guests, name='my_guests'),
    path('add_guest/', user_views.add_guest, name='add_guest'),
    path('guest_home/',user_views.guest_home, name='guest_home'),
    path('settings/',user_views.settings, name='settings'),
    path('logout/', user_views.logout_view, name='logout'),
    path('guest_logout_view/', user_views.guest_logout_view, name='guest_logout_view'),
    path("password_reset_view/", user_views.password_reset_view, name="password_reset_view"),
    path("account/", user_views.account, name="account"),
    path("delete_account/", user_views.delete_account, name="delete_account"),
    path("contact_support/", user_views.contact_support, name="contact_support"),
    
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
    path('update_device_state/<str:device_id>/', device_views.update_device_state, name='update_device_state'),
    path('device/<str:device_id>/', device_views.device_info, name='device_info'),
    
    path('energy_home/', energy_views.energy_home, name='energy_home'),
    path('set_goal/', energy_views.set_goal, name='set_goal'),
    path('remove_goal/', energy_views.remove_goal, name='remove_goal'),
    path('usage_stats/', energy_views.usage_stats, name='usage_stats'),
    path('join_event/<int:event_id>/', energy_views.join_event, name='join_event'),
    path('leave_event/<int:event_id>/', energy_views.leave_event, name='leave_event'),
    
    path('modes_list/', ambiance_views.modes_list, name='modes_list'),
    path('toggle_ambiance/<int:mode_id>/', ambiance_views.toggle_ambiance, name='toggle_ambiance'),
    path('add_ambiance_mode/', ambiance_views.add_ambiance_mode, name='add_ambiance_mode'),
    path('edit_ambiance_mode/<int:mode_id>/', ambiance_views.edit_ambiance_mode, name='edit_ambiance_mode'),
    path('mode_details/<int:mode_id>/', ambiance_views.mode_details, name='mode_details'),
    path('delete_ambiance_mode/<int:mode_id>/', ambiance_views.delete_ambiance_mode, name='delete_ambiance_mode'),
    
    path('automations_list/', automation_views.automations_list, name='automations_list'),
    path('add_automation/', automation_views.add_automation, name='add_automation'),
    path('edit_automation/<int:automation_id>/', automation_views.edit_automation, name='edit_automation'),
    path('delete_automation/<int:automation_id>/', automation_views.delete_automation, name='delete_automation'),
    path('automation_details/<int:automation_id>/', automation_views.automation_details, name='automation_details'), 

    path('ds_main/', ds_views.ds_main, name='ds_main'),
    path('add_listing/', ds_views.add_listing, name='add_listing'),
    path('remove_listing/<int:device_id>/', ds_views.remove_listing, name='remove_listing'),
    path('approve_request/<int:req_id>/', ds_views.approve_request, name='approve_request'),
    path('decline_request/<int:req_id>/', ds_views.decline_request, name='decline_request'),
    path('search_results/', ds_views.search_results, name='search_results'),
    path('request/<int:listing_id>/', ds_views.create_request, name='create_request'),
]
