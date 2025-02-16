# notifs/views.py

from django.shortcuts import render, redirect
from .models import Notification

def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user, is_read=False)

    # Mark notifications as read when viewed
    notifications.update(is_read=True)

    return render(request, 'notifs/notifications_list.html', {'notifications': notifications})
