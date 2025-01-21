from django.contrib import admin
from .models import EnergyGoal, EnergyUsage, IntervalReading, CommunityEvent

admin.site.register(EnergyGoal)
admin.site.register(EnergyUsage)
admin.site.register(IntervalReading)
admin.site.register(CommunityEvent)

