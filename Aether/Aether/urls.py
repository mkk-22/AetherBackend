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
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.start, name='start'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.ownerlogin, name='ownerlogin'),
    path('guest_login/', views.guest_login, name='guest_login'),
    path('home/', views.home, name='home'),
    path('my_guests/', views.my_guests, name='my_guests'),
    path('generate_guest_code/', views.generate_guest_code, name='generate_guest_code'),
    path('guest_home/', views.guest_home, name='guest_home'),
    path('logout/', views.logout_view, name='logout')
]
