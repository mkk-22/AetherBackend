# energy/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import EnergyGoal, UserEnergyUsage, DeviceEnergyUsage, IntervalReading, CommunityEvent
from devices.models import House
from devices.device_views import calculate_usage
from .forms import EnergyGoalForm
from django.utils.timezone import now
from django.db.models import F
from django.db.models import Sum
from datetime import datetime, timedelta

from decimal import Decimal

from decimal import Decimal, ROUND_DOWN

from decimal import Decimal, ROUND_DOWN
from datetime import timedelta

from decimal import Decimal, ROUND_DOWN
from datetime import timedelta

@login_required
def energy_home(request):
    goal = EnergyGoal.objects.filter(homeowner=request.user.owner).first()

    daily_usage = UserEnergyUsage.objects.filter(homeowner=request.user.owner, creation_timestamp__date=now().date()).aggregate(total=Sum('total_consumption'))
    daily_progress = daily_usage['total'] if daily_usage['total'] else 0

    events = CommunityEvent.objects.all()
    
    start_of_month = now().replace(day=1)
    total_usage_month_so_far = UserEnergyUsage.objects.filter(homeowner=request.user.owner, creation_timestamp__gte=start_of_month).aggregate(total=Sum('total_consumption'))['total'] or 0

    start_of_year = now().replace(month=1, day=1)
    total_usage_year_so_far = UserEnergyUsage.objects.filter(homeowner=request.user.owner, creation_timestamp__gte=start_of_year).aggregate(total=Sum('total_consumption'))['total'] or 0

    days_in_month = (start_of_month.replace(month=now().month % 12 + 1) - start_of_month).days
    days_so_far = (now().date() - start_of_month.date()).days
    months_in_year = 12
    months_so_far = (now().month - 1)

    if days_so_far > 0:
        projected_usage_month = (total_usage_month_so_far / days_so_far) * days_in_month
    else:
        projected_usage_month = 0

    if months_so_far > 0:
        projected_usage_year = (total_usage_year_so_far / months_so_far) * months_in_year
    else:
        projected_usage_year = 0

    cost_per_kwh = 0.20
    cost_per_kwh = Decimal(cost_per_kwh)

    projected_cost_month = projected_usage_month * cost_per_kwh
    projected_cost_year = projected_usage_year * cost_per_kwh

    projected_cost_month = projected_cost_month.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    projected_cost_year = projected_cost_year.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    projected_usage_month = projected_usage_month.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    projected_usage_year = projected_usage_year.quantize(Decimal('0.01'), rounding=ROUND_DOWN)

    return render(request, 'energy_home.html',{'goal': goal, 'daily_progress': daily_progress, 'events': events, 'projected_usage_month': projected_usage_month, 'projected_usage_year': projected_usage_year, 'projected_cost_month': projected_cost_month, 'projected_cost_year': projected_cost_year})


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
    user = request.user
    today = now().date()

    # Hourly Usage for Today
    hourly_usage = []
    for hour in range(24):  # Loop through 24 hours
        consumption = UserEnergyUsage.objects.filter(
            homeowner=user.owner, 
            creation_timestamp__hour=hour, 
            creation_timestamp__date=today
        ).aggregate(total=Sum('total_consumption'))['total'] or 0
        hourly_usage.append((hour, consumption))

    # Daily Usage for This Week (from Sunday)
    daily_usage = []
    for i in range(7):  # Loop through the past 7 days of the week
        day = today - timedelta(days=(today.weekday() - i +1) % 7)
        consumption = UserEnergyUsage.objects.filter(
            homeowner=user.owner, 
            creation_timestamp__date=day
        ).aggregate(total=Sum('total_consumption'))['total'] or 0
        daily_usage.append((day.strftime('%A'), consumption))

    # Weekly Usage for This Month (Since the 1st)
    weekly_usage = []
    for week in range(1, 6):  # Loop through the first 5 weeks of the month
        # Calculate week start and end dates
        week_start = today.replace(day=1) + timedelta(weeks=week-1)
        week_end = week_start + timedelta(days=6)
        consumption = UserEnergyUsage.objects.filter(
            homeowner=user.owner, 
            creation_timestamp__gte=week_start, 
            creation_timestamp__lte=week_end
        ).aggregate(total=Sum('total_consumption'))['total'] or 0
        weekly_usage.append((f"Week {week}", consumption))

    # Monthly Usage for This Year
    monthly_usage = []
    for month in range(1, 13):  # Loop through all 12 months
        consumption = UserEnergyUsage.objects.filter(
            homeowner=user.owner, 
            creation_timestamp__month=month, 
            creation_timestamp__year=today.year
        ).aggregate(total=Sum('total_consumption'))['total'] or 0
        monthly_usage.append((month, consumption))

    # Yearly Usage for the Past 5 Years
    yearly_usage = []
    for year in range(today.year - 5, today.year + 1):  # Loop through the past 5 years
        consumption = UserEnergyUsage.objects.filter(
            homeowner=user.owner, 
            creation_timestamp__year=year
        ).aggregate(total=Sum('total_consumption'))['total'] or 0
        yearly_usage.append((year, consumption))

    context = {
        'hourly_usage': hourly_usage,
        'daily_usage': daily_usage,
        'weekly_usage': weekly_usage,
        'monthly_usage': monthly_usage,
        'yearly_usage': yearly_usage,
    }

    return render(request, 'usage_stats.html', context)

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

def hourly_calculation():
    houses = House.objects.all()
    
    for house in houses:
        devices = house.devices.all()
        for device in devices:
            if device.status == 'off':  
                continue  # Skip if device is off

            # Close old interval
            interval = IntervalReading.objects.filter(
                device_id=device.device_id,
                end__isnull=True  
            ).first()
            
            if interval:  
                interval.end = now()
                interval.usage = calculate_usage(interval)
                interval.save()

            # Create new interval
            IntervalReading.objects.create(
                device_id=device.device_id, 
                homeowner=house.owner,  
                start=now()
            )

            # Update usage
            DeviceEnergyUsage.objects.filter(device_id=device.device_id, creation_timestamp__hour=now().hour).update(total_consumption=F('total_consumption') + interval.usage)
            UserEnergyUsage.objects.filter(homeowner=house.owner, creation_timestamp__hour=now().hour).update(total_consumption=F('total_consumption') + interval.usage)

            DeviceEnergyUsage.objects.filter(device_id=device.device_id, creation_timestamp__date=now().date()).update(total_consumption=F('total_consumption') + interval.usage)
            UserEnergyUsage.objects.filter(homeowner=house.owner, creation_timestamp__date=now().date()).update(total_consumption=F('total_consumption') + interval.usage)

            DeviceEnergyUsage.objects.filter(device_id=device.device_id, creation_timestamp__month=now().month).update(total_consumption=F('total_consumption') + interval.usage)
            UserEnergyUsage.objects.filter(homeowner=house.owner, creation_timestamp__month=now().month).update(total_consumption=F('total_consumption') + interval.usage)

            DeviceEnergyUsage.objects.filter(device_id=device.device_id, creation_timestamp__year=now().year).update(total_consumption=F('total_consumption') + interval.usage)
            UserEnergyUsage.objects.filter(homeowner=house.owner, creation_timestamp__year=now().year).update(total_consumption=F('total_consumption') + interval.usage)

    return
  