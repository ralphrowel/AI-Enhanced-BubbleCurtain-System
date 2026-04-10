#admin.py

from django.contrib import admin
from .models import Device, Signal, Sensor

admin.site.register(Device)
admin.site.register(Signal)

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    pass