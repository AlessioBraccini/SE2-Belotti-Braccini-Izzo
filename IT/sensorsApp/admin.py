from django.contrib import admin
from .models import *

# Register your models here.


class HumiditySensorAdmin(admin.ModelAdmin):
    list_display = ('district', 'humidity', 'temperature')
admin.site.register(HumiditySensor, HumiditySensorAdmin)


class WaterIrrigationSensorAdmin(admin.ModelAdmin):
    list_display = ('district', 'water_qty')
admin.site.register(WaterIrrigationSensor, WaterIrrigationSensorAdmin)

