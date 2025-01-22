# energy/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import EnergyGoal, EnergyUsage, CommunityEvent
from .forms import EnergyGoalForm


@login_required
def energy_home(request):
    goal = EnergyGoal.objects.filter(homeowner=request.user.owner).first()
    
    daily_usage = EnergyUsage.objects.filter(homeowner=request.user.owner, period='daily').order_by('-creation_timestamp').first()
    
    events = CommunityEvent.objects.all()

    context = {
        'goal': goal,
        'daily_progress': daily_usage.total_consumption if daily_usage else 0,
        'events': events, 
    }
    return render(request, 'energy_home.html', context)

@login_required
def set_goal(request):
    if request.method == 'POST':
        form = EnergyGoalForm(request.POST)
        if form.is_valid():
            goal, created = EnergyGoal.objects.update_or_create(
                homeowner=request.user.owner,
                defaults={'goal': form.cleaned_data['goal']}
            )
            return redirect('energy_home')
    else:
        form = EnergyGoalForm()
    return render(request, 'set_goal.html', {'form': form})

@login_required
def remove_goal(request):
    EnergyGoal.objects.filter(homeowner=request.user.owner).delete()
    return redirect('energy_home')

@login_required
def usage_stats(request):
    usage = EnergyUsage.objects.filter(homeowner=request.user.owner).order_by('-creation_timestamp')
    return render(request, 'usage_stats.html', {'usage': usage})

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CommunityEvent

@login_required
def join_event(request, event_id):
    event = get_object_or_404(CommunityEvent, id=event_id)
    event.joined = True
    event.save()
    return redirect('energy_home')

@login_required
def leave_event(request, event_id):
    event = get_object_or_404(CommunityEvent, id=event_id)
    event.joined = False
    event.save()
    return redirect('energy_home')

